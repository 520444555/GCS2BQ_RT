cm_event_state_updates={
    "type":"object",
    "properties":{
        "userId" :{"type":["string","null"]},
        "stateMachineId" :{"type":["string","null"]},
        "@version" :{"type":["string","null"]},
        "@timestamp" :{"type":["string","null"]},
        "updatedAt" :{"type":["integer","null"]},
        "username":{"type":["string","null"]},
        "notificationVersion":{"type":["string","null"]},
        "state": {
                  "type":"object",
                  "properties":{
                                "id":{"type":["string","null"]},
                   }
         },
"reasons":{
                   "type":"array",
                   "items":{
                             "type":"object",
                             "properties":{
                                       "id":{"type":["string","null"]},
                                       "statusid":{"type":["string","null"]},
                                       "name":{"type":["string","null"]},
                                      },
                                },
         },
        "ids":{
                   "type":"array",
                   "items":{
                             "type":"object",
"properties":{
                                       "channelId":{"type":["string","null"]},
                                       "identifier":{"type":["string","null"]},
                                       "timestamp":{"type":["integer","null"]},
                                       "payload": {
                                                    "type":"object",
                                                    "properties":{
                                                                    "schema":{  
                                                                            "type":"object",
                                                                            "properties":{
                                                                                "alert_id":{"type":["string","null"]},
                                                                                "event_type":{"type":["string","null"]},
                                                                                "lifecycle_id":{"type":["string","null"]},
                                                                                "pib_suspended":{"type":["string","null"]},
                                                                                "customer_id":{"type":["string","null"]},
},
                                                                    
                                                                    },
                                                                },
                                               },
                                      },
                                },
        },
        "note":{"type":["string","null"]},
    },
    "required":["@version","@timestamp"],
}



cm_case_queue_change={

    "type":"object",
    "properties":{
        "@version" :{"type":["string","null"]},
        "ids":{
        "type":"array",
        "items":{
                    "type":"object",
                    "properties":{
                            "channelId":{"type":["string","null"]},
                            "identifier":{"type":["string","null"]},
                            "timestamp":{"type":["integer","null"]},
                    },
                },

        },
        "notificationVersion":{"type":["string","null"]},
        "queueId":{"type":["string","null"]},
        "updatedAt":{"type":["integer","null"]},
        "queueName":{"type":["string","null"]},
        "@timestamp":{"type":["string","null"]},
      },
    "required":["@version","@timestamp"],


}
