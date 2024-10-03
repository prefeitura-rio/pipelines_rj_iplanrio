from pyarrow import string
from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "displayName": 1,
            "fullName": 1,
            "email": 1,
            "phoneNumber": 1,
            "cpf": 1,
            "createdAt": {"$toString": "$createdAt"},
            "birthDate": {"$toString": "$birthDate"},
            "federalRevenueData": 1,
            "validadoReceita": {"$toString": "$validadoReceita"},
        },
    },
    {"$unset": "_id"},
    {
        "$project": {
            "id": 1,
            "displayName": 1,
            "fullName": 1,
            "email": 1,
            "phoneNumber": 1,
            "cpf": 1,
            "createdAt": 1,
            "birthDate": 1,
            "validadoReceita": 1,
            "federalRevenueData": {
                "$function": {
                    "lang": "js",
                    "args": ["$federalRevenueData"],
                    "body": "function(federalRevenueData) { return JSON.stringify(federalRevenueData); }",
                },
            },
        },
    },
]

schema = Schema(
    {
        "id": string(),
        "displayName": string(),
        "fullName": string(),
        "email": string(),
        "phoneNumber": string(),
        "cpf": string(),
        "createdAt": string(),
        "birthDate": string(),
        "validadoReceita": string(),
        "federalRevenueData": string(),
    },
)
