import logging
import apache_beam as beam
from resources import table_list


class getdata(beam.DoFn):
        def process(self,element,logging_mode):
                logging.getLogger().setLevel(logging.getLevelName(logging_mode))
                from apache_beam import pvalue
                #Getting the full name of the file
                full_name=str(element)
                #Adding logging
                logging.info('file name pattern matching ------------------: %s ', full_name)
                #Getting file name
                file_name=full_name.rsplit("/",1)[-1]
          
                #Mapping of file names
                condition_mapping = {"CM_UPDATES_EVENTS-EVENT":"CM_UPDATES_EVENTS_EVENT","CM_UPDATES_EVENTS-QUEUE":"CM_UPDATES_EVENTS_QUEUE","CM_UPDATES_EVENTS-STATUS":"CM_UPDATES_EVENTS_STATUS","CM_UPDATES_EVENTS-USER":"CM_UPDATES_EVENTS_USER","CM_UPDATES_CASES-EVENT":"CM_UPDATES_CASES_EVENT","CM_UPDATES_CASES-QUEUE":"CM_UPDATES_CASES_QUEUE","CM_UPDATES_CASES-USER":"CM_UPDATES_CASES_USER","CM_UPDATES_CASES-STATE":"CM_UPDATES_CASES_STATE","CM_UPDATES_CASES-CASE":"CM_UPDATES_CASES_CASES","CM_UPDATES_EVENTS-NOTES":"CM_ADD_NOTE"}

                result = next((value for condition, value in condition_mapping.items() if condition in file_name), "none")
                if result != "none":
                        #File is correct
                        #Tag correct output
                        yield pvalue.TaggedOutput(result, full_name)
                else:
                        #Incorrect file
                        incorrect_file = {}
                        incorrect_file['input_file_name'] = full_name
                        incorrect_file['target_table_name'] = ""
                        incorrect_file['error_message'] = "FILE NAME NOT MATCHING PATTERN"
                        incorrect_file['event_data'] = "FILE NAME NOT MATCHING PATTERN"
                        #Tag error JSON
                        yield pvalue.TaggedOutput('file_not_found', incorrect_file)
