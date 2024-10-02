from pyarrow import string
from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "description": 1,
            "value": {"$toString": "$value"},
            "createdAt": {"$toString": "$createdAt"},
        },
    },
    {
        "$unset": "_id",
    },
]

schema = Schema(
    {
        "id": string(),
        "description": string(),
        "value": string(),
        "createdAt": string(),
    },
)
