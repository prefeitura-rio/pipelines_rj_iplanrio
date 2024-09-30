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
        "id": str,
        "pindex": int,
        "name": str,
        "type": str,
    },
)
