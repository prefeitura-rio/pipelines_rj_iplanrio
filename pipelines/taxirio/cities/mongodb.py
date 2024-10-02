from pyarrow import string
from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "name": 1,
            "stateAbbreviation": 1,
            "isCalulatedInApp": {"$toString": "$isCalulatedInApp"},
            "isAbleToUsePaymentInApp": {"$toString": "$isAbleToUsePaymentInApp"},
            "loginLabel": 1,
            "serviceStations": {
                "$function": {
                    "lang": "js",
                    "args": ["$serviceStations"],
                    "body": "function(serviceStations) { return JSON.stringify(serviceStations); }",
                },
            },
            "geometry": {
                "$function": {
                    "lang": "js",
                    "args": ["$geometry"],
                    "body": "function(geometry) { return JSON.stringify(geometry); }",
                },
            },
        },
    },
    {"$unset": "_id"},
]

schema = Schema(
    {
        "id": string(),
        "name": string(),
        "stateAbbreviation": string(),
        "isCalulatedInApp": string(),
        "isAbleToUsePaymentInApp": string(),
        "loginLabel": string(),
        "serviceStations": string(),
        "geometry": string(),
    },
)
