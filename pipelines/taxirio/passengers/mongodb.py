from pyarrow import string
from pymongoarrow.api import Schema

pipeline = [
    {
        "$project": {
            "id": {"$toString": "$_id"},
            "user": {"$toString": "$user"},
            "createdAt": {"$toString": "$createdAt"},
            "login": 1,
            "password": 1,
            "salt": 1,
            "isAbleToUsePaymentInApp": {"$toString": "$isAbleToUsePaymentInApp"},
            "tokenInfo": 1,
            "infoPhone": 1,
            "validadoReceita": {"$toString": "$validadoReceita"},
            "ano_particao": {"$toString": {"$year": "$createdAt"}},
            "mes_particao": {"$toString": {"$month": "$createdAt"}},
        },
    },
    {"$unset": "_id"},
    {
        "$project": {
            "id": 1,
            "user": 1,
            "createdAt": 1,
            "login": 1,
            "password": 1,
            "salt": 1,
            "isAbleToUsePaymentInApp": 1,
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
        "displayName": string(),
        "fullName": string(),
        "email": string(),
        "phoneNumber": string(),
        "cpf": string(),
        "createdAt": string(),
        "birthDate": string(),
        "validadoReceita": string(),
        "tokenInfo": string(),
        "ano_particao": string(),
        "mes_particao": string(),
    },
)
