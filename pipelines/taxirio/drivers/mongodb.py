from datetime import datetime

from pyarrow import list_, string
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
        "id": str,
        "user": str,
        "taxiDriverId": str,
        "cars": list_(string()),
        "average": float,
        "associatedCar": str,
        "createdAt": datetime,
        "status": str,
        "associatedDiscount": str,
        "associatedPaymentsMethods": list_(string()),
        "login": str,
        "password": str,
        "salt": str,
        "isAbleToReceivePaymentInApp": bool,
        "isAbleToReceivePaymentInCityHall": bool,
        "ratingsReceived": int,
        "busy": bool,
        "associatedRace": {
            "originAtAccepted": {
                "position": {
                    "lng": float,
                    "lat": float,
                },
            },
            "race": str,
        },
        "lastAverage": int,
        "expiredBlockByRankingDate": datetime,
        "blockedRace": str,
        "infoPhone": {
            "updatedAt": datetime,
            "_id": str,
            "appVersion": str,
            "phoneModel": str,
            "phoneManufacturer": str,
            "osVersion": str,
            "osName": str,
        },
        "tokenInfo": {
            "httpSalt": str,
            "wssSalt": str,
            "pushToken": str,
        },
        "city": str,
        "serviceRecordRate": float,
        "nota": float,
        "averageTT": float,
    },
)
