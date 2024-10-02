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
            "createdAt": {"$toString": "$createdAt"},
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
    {"$unset": "_id"},
    {
        "$project": {
            "id": 1,
            "associatedCar": 1,
            "associatedDiscount": 1,
            "average": 1,
            "averageTT": 1,
            "blockedRace": 1,
            "busy": 1,
            "city": 1,
            "createdAt": 1,
            "expiredBlockByRankingDate": 1,
            "isAbleToReceivePaymentInApp": 1,
            "isAbleToReceivePaymentInCityHall": 1,
            "lastAverage": 1,
            "login": 1,
            "nota": 1,
            "password": 1,
            "ratingsReceived": 1,
            "salt": 1,
            "serviceRecordRate": 1,
            "status": 1,
            "taxiDriverId": 1,
            "user": 1,
            "cars": {
                "$function": {
                    "lang": "js",
                    "args": ["$cars"],
                    "body": "function(cars) { return JSON.stringify(cars); }",
                },
            },
            "associatedPaymentsMethods": {
                "$function": {
                    "lang": "js",
                    "args": ["$associatedPaymentsMethods"],
                    "body": "function(associatedPaymentsMethods) { return JSON.stringify(associatedPaymentsMethods); }",
                },
            },
            "associatedRace": {
                "$function": {
                    "lang": "js",
                    "args": ["$associatedRace"],
                    "body": "function(associatedRace) { return JSON.stringify(associatedRace); }",
                },
            },
            "infoPhone": {
                "$function": {
                    "lang": "js",
                    "args": ["$infoPhone"],
                    "body": "function(infoPhone) { return JSON.stringify(infoPhone); }",
                },
            },
            "tokenInfo": {
                "$function": {
                    "lang": "js",
                    "args": ["$tokenInfo"],
                    "body": "function(tokenInfo) { return JSON.stringify(tokenInfo); }",
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
    },
)