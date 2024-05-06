#any configurations to the pipeline ex: database connectivity etc
table_name='hsbc-10534429-fdreu-dev:FZ_EU_FDR_DEV.event_store'
create_disposition='CREATE_NEVER'
write_disposition='WRITE_APPEND'
ignore_unknown_columns=True
method='STREAMING_INSERTS'
