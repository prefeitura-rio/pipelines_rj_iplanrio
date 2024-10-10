from pyarrow import string
from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "user": {"$toString": "$user"},
            "taxiDriverId": 1,
            "cars": {
                "$map": {
                    "input": "$cars",
                    "as": "car",
                    "in": {"$toString": "$$car"},
                },
            },
            "average": {"$toString": "$average"},
            "associatedCar": {"$toString": "$associatedCar"},
            "createdAt": {"$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}},
            "ano_particao": {"$dateToString": {"format": "%Y", "date": "$createdAt"}},
            "mes_particao": {"$dateToString": {"format": "%m", "date": "$createdAt"}},
            "status": 1,
            "associatedDiscount": {"$toString": "$associatedDiscount"},
            "associatedPaymentsMethods": {
                "$map": {
                    "input": "$associatedPaymentsMethods",
                    "as": "paymentMethod",
                    "in": {"$toString": "$$paymentMethod"},
                },
            },
            "login": 1,
            "password": 1,
            "salt": 1,
            "isAbleToReceivePaymentInApp": {"$toString": "$isAbleToReceivePaymentInApp"},
            "isAbleToReceivePaymentInCityHall": {"$toString": "$isAbleToReceivePaymentInCityHall"},
            "ratingsReceived": {"$toString": "$ratingsReceived"},
            "busy": {"$toString": "$busy"},
            "associatedRace": {
                "originAtAccepted": {
                    "position": {
                        "lng": "$associatedRace.originAtAccepted.position.lng",
                        "lat": "$associatedRace.originAtAccepted.position.lat",
                    },
                },
                "race": {"$toString": "$associatedRace.race"},
            },
            "lastAverage": {"$toString": "$lastAverage"},
            "expiredBlockByRankingDate": {"$toString": "$expiredBlockByRankingDate"},
            "blockedRace": {"$toString": "$blockedRace"},
            "infoPhone": {
                "updatedAt": "$infoPhone.updatedAt",
                "id": {"$toString": "$infoPhone._id"},
                "appVersion": "$infoPhone.appVersion",
                "phoneModel": "$infoPhone.phoneModel",
                "phoneManufacturer": "$infoPhone.phoneManufacturer",
                "osVersion": "$infoPhone.osVersion",
                "osName": "$infoPhone.osName",
            },
            "tokenInfo": 1,
            "city": {"$toString": "$city"},
            "serviceRecordRate": {"$toString": "$serviceRecordRate"},
            "nota": {"$toString": "$nota"},
            "averageTT": {"$toString": "$averageTT"},
        },
    },
    {
        "$unset": "_id",
    },
    {
        "$addFields": {
            "cars": {
                "$function": {
                    "lang": "js",
                    "args": ["$cars"],
                    "body": "function(x) { return JSON.stringify(x); }",
                },
            },
            "associatedPaymentsMethods": {
                "$function": {
                    "lang": "js",
                    "args": ["$associatedPaymentsMethods"],
                    "body": "function(x) { return JSON.stringify(x); }",
                },
            },
            "associatedRace": {
                "$function": {
                    "lang": "js",
                    "args": ["$associatedRace"],
                    "body": "function(x) { return JSON.stringify(x); }",
                },
            },
            "infoPhone": {
                "$function": {
                    "lang": "js",
                    "args": ["$infoPhone"],
                    "body": "function(x) { return JSON.stringify(x); }",
                },
            },
            "tokenInfo": {
                "$function": {
                    "lang": "js",
                    "args": ["$tokenInfo"],
                    "body": "function(x) { return JSON.stringify(x); }",
                },
            },
        },
    },
]


schema = Schema(
    {
        "id": string(),
        "user": string(),
        "taxiDriverId": string(),
        "cars": string(),
        "average": string(),
        "associatedCar": string(),
        "createdAt": string(),
        "status": string(),
        "associatedDiscount": string(),
        "associatedPaymentsMethods": string(),
        "login": string(),
        "password": string(),
        "salt": string(),
        "isAbleToReceivePaymentInApp": string(),
        "isAbleToReceivePaymentInCityHall": string(),
        "ratingsReceived": string(),
        "busy": string(),
        "associatedRace": string(),
        "lastAverage": string(),
        "expiredBlockByRankingDate": string(),
        "blockedRace": string(),
        "infoPhone": string(),
        "tokenInfo": string(),
        "city": string(),
        "serviceRecordRate": string(),
        "nota": string(),
        "averageTT": string(),
        "ano_particao": string(),
        "mes_particao": string(),
    },
)
