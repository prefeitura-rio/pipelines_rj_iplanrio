from pyarrow import string
from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "updatedAt": {"$toString": "$updatedAt"},
            "createdAt": {"$toString": "$createdAt"},
            "race": {"$toString": "$race"},
            "ano_particao": {"$toString": {"$year": "$createdAt"}},
            "mes_particao": {"$toString": {"$month": "$createdAt"}},
            "competitors": {
                "$map": {
                    "input": "$competitors",
                    "as": "competitor",
                    "in": {
                        "driver": {"$toString": "$$competitor.driver"},
                        "id": {"$toString": "$$competitor._id"},
                        "rankingRaceStatus": "$$competitor.rankingRaceStatus",
                        "acceptedLocation": {
                            "$cond": {
                                "if": {"$ne": ["$$competitor.acceptedLocation", "NA"]},
                                "then": {
                                    "formattedAddress": "$$competitor.acceptedLocation.formattedAddress",
                                    "lat": {"$toString": "$$competitor.acceptedLocation.lat"},
                                    "lng": {"$toString": "$$competitor.acceptedLocation.lng"},
                                },
                                "else": "NA",
                            },
                        },
                        "distance": {
                            "$cond": {
                                "if": {"$ne": ["$$competitor.distance", "NA"]},
                                "then": {"$toString": "$$competitor.distance"},
                                "else": "NA",
                            },
                        },
                    },
                },
            },
        },
    },
    {"$unset": "_id"},
    {
        "$project": {
            "id": 1,
            "createdAt": 1,
            "updatedAt": 1,
            "race": 1,
            "ano_particao": 1,
            "mes_particao": 1,
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
