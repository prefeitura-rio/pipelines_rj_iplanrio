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
            "createdAt": {"$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}},
            "birthDate": {"$dateToString": {"format": "%Y-%m-%d", "date": "$birthDate"}},
            "federalRevenueData": 1,
            "validadoReceita": {"$toString": "$validadoReceita"},
            "ano_particao": {"$dateToString": {"format": "%Y", "date": "$createdAt"}},
            "mes_particao": {"$dateToString": {"format": "%m", "date": "$createdAt"}},
        },
    },
    {
        "$unset": "_id",
    },
    {
        "$addFields": {
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
        "ano_particao": string(),
        "mes_particao": string(),
    },
)
