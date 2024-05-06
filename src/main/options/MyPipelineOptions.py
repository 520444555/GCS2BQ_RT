import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions

class MyPipelineOptions(PipelineOptions):
  @classmethod
  def _add_argparse_args(cls, parser):
    parser.add_argument('--cm_updates_event_table')
    parser.add_argument('--cm_updates_queue_table')
    parser.add_argument('--cm_updates_status_table')
    parser.add_argument('--cm_updates_user_table')
    parser.add_argument('--cm_cases_user_table')
    parser.add_argument('--cm_cases_queue_table')
    parser.add_argument('--cm_cases_event_table')
    parser.add_argument('--cm_updates_cases_status_table')
    parser.add_argument('--cm_updates_cases_cases_table')
    parser.add_argument('--cm_add_note_table')
    parser.add_argument('--logging_mode',default='INFO')
    parser.add_argument('--subscription')
    parser.add_argument('--case_manager_error_table')
