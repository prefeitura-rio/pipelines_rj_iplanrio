import pyarrow as pa
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
        "$addFields": {
            "geometry": {
                "$cond": {
                    "if": {"$eq": ["$geometry.type", "Polygon"]},
                    "then": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            "$geometry.coordinates",
                        ],
                    },
                    "else": "$geometry",
                },
            },
        },
    },
    {
        "$unset": "_id",
    },
]

schema = Schema(
    {
        "id": pa.string(),
        "name": pa.string(),
        "stateAbbreviation": pa.string(),
        "isCalulatedInApp": pa.bool_(),
        "isAbleToUsePaymentInApp": pa.bool_(),
        "loginLabel": pa.string(),
        "serviceStations": pa.list_(
            pa.struct(
                [
                    ("name", pa.string()),
                    ("address", pa.string()),
                ],
            ),
        ),
        "geometry": {
            "type": pa.string(),
            "coordinates": pa.list_(pa.list_(pa.list_(pa.list_(pa.float64())))),
        },
    },
)
