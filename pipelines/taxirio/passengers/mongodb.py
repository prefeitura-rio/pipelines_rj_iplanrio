from pyarrow import string
from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "user": {"$toString": "$user"},
            "createdAt": {"$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}},
            "login": 1,
            "password": 1,
            "salt": 1,
            "isAbleToUsePaymentInApp": {"$toString": "$isAbleToUsePaymentInApp"},
            "tokenInfo": 1,
            "infoPhone": 1,
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
            "tokenInfo": {
                "$function": {
                    "lang": "js",
                    "args": ["$tokenInfo"],
                    "body": "function(tokenInfo) { return JSON.stringify(tokenInfo); }",
                },
            },
            "infoPhone": {
                "$function": {
                    "lang": "js",
                    "args": ["$infoPhone"],
                    "body": "function(infoPhone) { return JSON.stringify(infoPhone); }",
                },
            },
        },
    },
]

schema = Schema(
    {
        "id": string(),
        "user": string(),
        "createdAt": string(),
        "login": string(),
        "password": string(),
        "salt": string(),
        "isAbleToUsePaymentInApp": string(),
        "tokenInfo": string(),
        "infoPhone": string(),
        "validadoReceita": string(),
        "ano_particao": string(),
        "mes_particao": string(),
    },
)
