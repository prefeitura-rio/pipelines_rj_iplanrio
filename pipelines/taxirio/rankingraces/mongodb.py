from datetime import datetime
from typing import Any

from pyarrow import string
from pymongoarrow.api import Schema


def generate_pipeline(start: datetime, end: datetime) -> list[dict[str, Any]]:
    return [
        {
            "$match": {
                "createdAt": {
                    "$gte": start,
                    "$lt": end,
                },
            },
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "createdAt": {"$dateToString": {"date": "$createdAt"}},
                "updatedAt": {"$dateToString": {"date": "$updatedAt"}},
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
                            "acceptedLocation": "$$competitor.acceptedLocation",
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
                        "body": "function(x) { return JSON.stringify(x); }",
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
