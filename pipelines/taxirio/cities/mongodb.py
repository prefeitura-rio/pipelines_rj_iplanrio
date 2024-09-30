from pyarrow import float64, list_, string, struct
from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "name": 1,
            "stateAbbreviation": 1,
            "isCalulatedInApp": 1,
            "isAbleToUsePaymentInApp": 1,
            "loginLabel": 1,
            "serviceStations": 1,
            "geometry": 1,
        },
    },
    {
        "$unset": "_id",
    },
]

schema = Schema(
    {
        "id": str,
        "name": str,
        "stateAbbreviation": str,
        "isCalulatedInApp": bool,
        "isAbleToUsePaymentInApp": bool,
        "loginLabel": str,
        "serviceStations": list_(struct([("name", string()), ("address", string())])),
        "geometry": {
            "type": str,
            "coordinates": list_(list_(list_(float64()))),
        },
    },
)
