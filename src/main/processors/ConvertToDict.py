import json
import apache_beam as beam
import logging
from resources import tables_schema
import jsonschema
import fastjsonschema

class ConvertToDict(beam.DoFn):
        def __init__(self):
                super(self.__class__, self).__init__()
        def process(self,element,logging_mode,table_name):
                from apache_beam import pvalue
                #Creating fastjson attribute
                if not hasattr(self,'validate_cm_event_arrival'):
                        self.validate_cm_event_arrival=fastjsonschema.compile(tables_schema.cm_event_arrival)
                #Creating fastjson attribute
                if not hasattr(self,'validate_cm_event_state_updates'):
                        self.validate_cm_event_state_updates=fastjsonschema.compile(tables_schema.cm_event_state_updates)
                #Creating fastjson attribute
                if not hasattr(self,'validate_cm_event_queue_changed'):
                        self.validate_cm_event_queue_changed=fastjsonschema.compile(tables_schema.cm_event_queue_changed)
                #Creating fastjson attribute
                if not hasattr(self,'validate_cm_event_assignee_update'):
                        self.validate_cm_event_assignee_update=fastjsonschema.compile(tables_schema.cm_event_assignee_update)


                #Adding Logging
                 logging.getLogger().setLevel(logging.getLevelName(logging_mode))
                 logging.info('converttoDict filename-----%s',table_name.rsplit(".",1)[-1])
                 try:
                         #Loading row
                         row=json.loads(element)
                         logging.info('json load success ----------')
                         #Schema Validation
                         validation_name=eval("self.validate_"+table_name.rsplit(".",1)[-1])
                         validation_name(row)
                         #Correcting the Column Names
                         row['version']=row.pop('@version')
                         row['timestamp']=row.pop('@timestamp')
                         logging.debug(' json row : %s ',row)
                         logging.info("---------Validation successful for %s",table_name.rsplit(".",1)[-1])
                         #Tagging Output
                        yield pvalue.TaggedOutput('validated_row',row)
                except Exception as e:
                        #Creating Error JSON
                        logging.error("ALERT for PROJECT ID : %s JOB NAME: gcs-pubsub-bq-fdr-case-manager %s",table_name.rsplit(".")[0],str(e))
                        exception={}
                        exception['input_file_name']=table_name.rsplit(".",1)[-1]
                        exception['target_table_name']=table_name.rsplit(".",1)[-1]
                        exception['error_message']=str(e)
                        exception['event_data']=str(row)
                        #Exception row
                        yield  pvalue.TaggedOutput('exception_row',exception)
