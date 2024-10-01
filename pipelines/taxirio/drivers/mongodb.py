import pyarrow as pa
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
            "average": 1,
            "associatedCar": {"$toString": "$associatedCar"},
            "createdAt": 1,
            "status": {"$toString": "$status"},
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
            "isAbleToReceivePaymentInApp": 1,
            "isAbleToReceivePaymentInCityHall": 1,
            "ratingsReceived": 1,
            "busy": 1,
            "associatedRace": {
                "originAtAccepted": {
                    "position": {
                        "lng": "$associatedRace.originAtAccepted.position.lng",
                        "lat": "$associatedRace.originAtAccepted.position.lat",
                    },
                },
                "race": {"$toString": "$associatedRace.race"},
            },
            "lastAverage": 1,
            "expiredBlockByRankingDate": 1,
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
            "serviceRecordRate": 1,
            "nota": 1,
            "averageTT": 1,
        },
    },
    {
        "$unset": "_id",
    },
]

schema = Schema(
    {
        "id": pa.string(),
        "user": pa.string(),
        "taxiDriverId": pa.string(),
        "cars": pa.list_(pa.string()),
        "average": pa.float64(),
        "associatedCar": pa.string(),
        "createdAt": pa.timestamp("ms"),
        "status": pa.string(),
        "associatedDiscount": pa.string(),
        "associatedPaymentsMethods": pa.list_(pa.string()),
        "login": pa.string(),
        "password": pa.string(),
        "salt": pa.string(),
        "isAbleToReceivePaymentInApp": pa.bool_(),
        "isAbleToReceivePaymentInCityHall": pa.bool_(),
        "ratingsReceived": pa.int64(),
        "busy": pa.bool_(),
        "associatedRace": {
            "originAtAccepted": {
                "position": {
                    "lng": pa.float64(),
                    "lat": pa.float64(),
                },
            },
            "race": pa.string(),
        },
        "lastAverage": pa.int64(),
        "expiredBlockByRankingDate": pa.timestamp("ms"),
        "blockedRace": pa.string(),
        "infoPhone": {
            "updatedAt": pa.timestamp("ms"),
            "_id": pa.string(),
            "appVersion": pa.string(),
            "phoneModel": pa.string(),
            "phoneManufacturer": pa.string(),
            "osVersion": pa.string(),
            "osName": pa.string(),
        },
        "tokenInfo": {
            "httpSalt": pa.string(),
            "wssSalt": pa.string(),
            "pushToken": pa.string(),
        },
        "city": pa.string(),
        "serviceRecordRate": pa.float64(),
        "nota": pa.float64(),
        "averageTT": pa.float64(),
    },
)
