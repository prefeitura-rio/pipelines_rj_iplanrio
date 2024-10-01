import pyarrow as pa
from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "pindex": 1,
            "name": 1,
            "type": 1,
        },
    },
    {
        "$unset": "_id",
    },
]

schema = Schema(
    {
        "id": pa.string(),
        "pindex": pa.int64(),
        "name": pa.string(),
        "type": pa.string(),
    },
)
