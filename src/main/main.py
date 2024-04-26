import argparse
import logging
import json
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam as beam
from apache_beam import pvalue
from processors import ConvertToDict
from processors import getFile
from processors import getData
from options import MyPipelineOptions
from resources import tables_schema
import fastjsonschema
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'test'))
import test_main
import unittest
#only calling statements should be in here

if __name__ == '__main__':
      	logging.getLogger().setLevel(logging.INFO)
      	suite = unittest.TestLoader().loadTestsFromModule(test_main)
      	result_unittest = unittest.TextTestRunner().run(suite)
      	if result_unittest.wasSuccessful():
            		my_pipeline_options = PipelineOptions().view_as(MyPipelineOptions.MyPipelineOptions)
            		p = beam.Pipeline(options=PipelineOptions())
            		#List of Tables
            		tables_list=['CM_UPDATES_EVENTS_QUEUE','CM_UPDATES_EVENTS_EVENT','CM_UPDATES_EVENTS_STATUS','CM_UPDATES_EVENTS_USER','CM_CASES_USER','CM_CASES_QUEUE','CM_CASES_EVENT','CM_UPDATES_CASES_STATUS','CM_UPDATES_CASES_CASES','CM_ADD_NOTE','file_not_found']
            		#Reading from notifications
            		notification = (p | 'Read from PubSub' >> beam.io.ReadFromPubSub(subscription=my_pipeline_options.subscription))
                file_name = notification | 'Get file name' >> beam.Map(getFile.getfile)

            		#Getting the output tables
                        		file_type = file_name | 'Get file type' >> beam.ParDo(getData.getdata(),my_pipeline_options.logging_mode).with_outputs(*tables_list)                     
            
            		#Case for Events Event            
            		cm_updates_event = (file_type['CM_UPDATES_EVENTS_EVENT'] | 'read cm_updates_event' >> beam.io.ReadAllFromText()            
            		  	| 'convertToDict_cm_updates_event' >> beam.ParDo(ConvertToDict.ConvertToDict(),my_pipeline_options.logging_mode,my_pipeline_options.cm_updates_event_table).with_outputs('exception_row','validated_row'))
            		load_cm_updates_event= cm_updates_event['validated_row'] | 'loadtoBQ_cm_updates_event' >> beam.io.WriteToBigQuery(my_pipeline_options.cm_updates_event_table,ignore_unknown_columns=True,create_disposition='CREATE_NEVER',write_disposition='WRITE_APPEND',method='STREAMING_INSERTS',insert_retry_strategy='RETRY_ON_TRANSIENT_ERROR') 
                        load_cm_updates_event_error= cm_updates_event['exception_row'] | 'loadtoBQerror cm_updates_event' >> beam.io.WriteToBigQuery(my_pipeline_options.case_manager_error_table,ignore_unknown_columns=True,create_disposition='CREATE_NEVER',write_disposition='WRITE_APPEND',method='STREAMING_INSERTS',insert_retry_strategy='RETRY_ON_TRANSIENT_ERROR')

                        #Case for Event Status
            		cm_updates_status = (file_type['CM_UPDATES_EVENTS_STATUS'] | 'read cm_updates_status' >> beam.io.ReadAllFromText()
            			| ' convertToDict_cm_updates_status' >> beam.ParDo(ConvertToDict.ConvertToDict(),my_pipeline_options.logging_mode,my_pipeline_options.cm_updates_status_table).with_outputs('exception_row','validated_row'))
            		load_cm_updates_status=cm_updates_status['validated_row']	| 'loadtoBQ_cm_updates_status' >> beam.io.WriteToBigQuery(my_pipeline_options.cm_updates_status_table,ignore_unknown_columns=True,create_disposition='CREATE_NEVER',write_disposition='WRITE_APPEND',method='STREAMING_INSERTS',insert_retry_strategy='RETRY_ON_TRANSIENT_ERROR')
                        load_cm_updates_status_error=cm_updates_status['exception_row']	| 'loadtoBQerror cm_updates_status' >> beam.io.WriteToBigQuery(my_pipeline_options.case_manager_error_table,ignore_unknown_columns=True,create_disposition='CREATE_NEVER',write_disposition='WRITE_APPEND',method='STREAMING_INSERTS',insert_retry_strategy='RETRY_ON_TRANSIENT_ERROR')
                        #Case for Add Note
                        
                        cm_add_note = (file_type['CM_ADD_NOTE'] | 'read cm_add_note' >> beam.io.ReadAllFromText()                        
                        		| ' convertToDict_cm_add_note' >> beam.ParDo(ConvertToDict.ConvertToDict(),my_pipeline_options.logging_mode,my_pipeline_options.cm_add_note_table).with_outputs('exception_row','validated_row'))
                        load_cm_add_note=cm_add_note['validated_row'] | 'loadtoBQ_cm_add_note' >> beam.io.WriteToBigQuery(my_pipeline_options.cm_add_note_table,ignore_unknown_columns=True,create_disposition='CREATE_NEVER',write_disposition='WRITE_APPEND',method='STREAMING_INSERTS')
                        load_cm_add_note_error =cm_add_note['exception_row']|'loadtoBQerror cm_add_note' >> beam.io.WriteToBigQuery(my_pipeline_options.case_manager_error_table,ignore_unknown_columns=True,create_disposition='CREATE_NEVER',write_disposition='WRITE_APPEND',method='STREAMING_INSERTS')
                        
                        #Writing to Error table
                        
                        file_not_found=file_type['file_not_found'] |' pattern_not_found'  >> beam.io.WriteToBigQuery(my_pipeline_options.case_manager_error_table,ignore_unknown_columns=True,create_disposition='CREATE_NEVER',write_disposition='WRITE_APPEND',method='STREAMING_INSERTS')
                        
                        #Running the pipeline
                        
                        result = p.run()                        
                        result.wait_until_finish()
