import pyarrow as pa
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
        "id": pa.string(),
        "description": pa.string(),
        "value": pa.float64(),
        "createdAt": pa.timestamp("ms"),
    },
)
