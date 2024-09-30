from datetime import datetime

from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "description": 1,
            "value": 1,
            "createdAt": 1,
        },
    },
    {
        "$unset": "_id",
    },
]

schema = Schema(
    {
        "id": str,
        "description": str,
        "value": float,
        "createdAt": datetime,
    },
)
