from datetime import datetime
from functools import partial

from pyarrow import string
from pymongoarrow.api import Schema
from pytz import timezone

from pipelines.constants import constants

sp_datetime = partial(datetime, tzinfo=timezone(constants.TIMEZONE.value))

pipeline = [
    {
        "$match": {
            "createdAt": {
                "$gte": sp_datetime(2023, 1, 1),
                "$lt": sp_datetime(2024, 12, 31),
            },
        },
    },
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "createdAt": {"$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}},
            "updatedAt": {"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}},
            "race": {"$toString": "$race"},
            "ano_particao": {"$dateToString": {"format": "%Y", "date": "$createdAt"}},
            "mes_particao": {"$dateToString": {"format": "%m", "date": "$createdAt"}},
            "competitors": {
                "$map": {
                    "input": "$competitors",
                    "as": "competitor",
                    "in": {
                        "driver": {"$toString": "$$competitor.driver"},
                        "id": {"$toString": "$$competitor._id"},
                        "rankingRaceStatus": "$$competitor.rankingRaceStatus",
                        "distance": {"$toString": "$$competitor.distance"},
                        "acceptedLocation": {
                            "formattedAddress": "$$competitor.acceptedLocation.formattedAddress",
                            "lat": {"$toString": "$$competitor.acceptedLocation.lat"},
                            "lng": {"$toString": "$$competitor.acceptedLocation.lng"},
                        },
                    },
                },
            },
        },
    },
    {
        "$unset": "_id",
    },
    {
        "$addFields": {
            "competitors": {
                "$function": {
                    "lang": "js",
                    "args": ["$competitors"],
                    "body": "function(competitors) { return JSON.stringify(competitors); }",
                },
            },
        },
    },
]

schema = Schema(
    {
        "id": string(),
        "createdAt": string(),
        "updatedAt": string(),
        "race": string(),
        "ano_particao": string(),
        "mes_particao": string(),
        "competitors": string(),
    },
)
