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
                "event": {"$toString": "$event"},
                "estimatedDuration": {"$toString": "$estimatedDuration"},
                "passenger": {"$toString": "$passenger"},
                "city": {"$toString": "$city"},
                "broadcastQtd": {"$toString": "$broadcastQtd"},
                "rating": 1,
                "tolls": 1,
                "isSuspect": {"$toString": "$isSuspect"},
                "isInvalid": {"$toString": "$isInvalid"},
                "billing": {
                    "estimatedPrice": {"$toString": "$billing.estimatedPrice"},
                    "associatedPaymentMethod": {"$toString": "$billing.associatedPaymentMethod"},
                    "associatedTaximeter": {"$toString": "$billing.associatedTaximeter"},
                    "associatedMinimumFare": {"$toString": "$billing.associatedMinimumFare"},
                    "associatedDiscount": {"$toString": "$billing.associatedDiscount"},
                    "associatedCorporative": {
                        "externalPropertyPassenger": {
                            "$toString": "$billing.associatedCorporative.externalPropertyPassenger",
                        },
                    },
                },
                "geolocation": 1,
                "status": 1,
                "createdAt": {"$dateToString": {"date": "$createdAt"}},
                "finishedAt": {"$dateToString": {"date": "$finishedAt"}},
                "ano_particao": {"$dateToString": {"format": "%Y", "date": "$createdAt"}},
                "mes_particao": {"$dateToString": {"format": "%m", "date": "$createdAt"}},
                "routeOriginDestination": {
                    "distance": {
                        "text": "$routeOriginDestination.distance.text",
                        "value": "$routeOriginDestination.distance.value",
                    },
                    "duration": {
                        "text": "$routeOriginDestination.duration.text",
                        "value": "$routeOriginDestination.duration.value",
                    },
                },
            },
        },
        {
            "$unset": "_id",
        },
        {
            "$addFields": {
                "rating": {
                    "$function": {
                        "lang": "js",
                        "args": ["$rating"],
                        "body": "function(x) { return JSON.stringify(x); }",
                    },
                },
                "tolls": {
                    "$function": {
                        "lang": "js",
                        "args": ["$tolls"],
                        "body": "function(x) { return JSON.stringify(x); }",
                    },
                },
                "billing": {
                    "$function": {
                        "lang": "js",
                        "args": ["$billing"],
                        "body": "function(x) { return JSON.stringify(x); }",
                    },
                },
                "geolocation": {
                    "$function": {
                        "lang": "js",
                        "args": ["$geolocation"],
                        "body": "function(x) { return JSON.stringify(x); }",
                    },
                },
                "routeOriginDestination": {
                    "$function": {
                        "lang": "js",
                        "args": ["$routeOriginDestination"],
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
        "ano_particao": string(),
        "mes_particao": string(),
        "event": string(),
        "estimatedDuration": string(),
        "passenger": string(),
        "city": string(),
        "broadcastQtd": string(),
        "routeOriginDestination": string(),
        "rating": string(),
        "tolls": string(),
        "isSuspect": string(),
        "isInvalid": string(),
        "billing": string(),
        "geolocation": string(),
        "status": string(),
    },
)
