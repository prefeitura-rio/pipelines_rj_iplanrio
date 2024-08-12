SELECT
    CAST(idsetor AS INT64) AS idsetor,
    CAST(idorgao AS INT64) AS idorgao,
    CAST(sigla_orgao AS STRING) AS sigla_orgao,
    CAST(nome_orgao AS STRING) AS nome_orgao,
    CAST(sigla_setor AS STRING) AS sigla_setor,
    CAST(nome_setor AS STRING) AS nome_setor
FROM
    `rj-iplanrio.adm_processo_interno_processorio_staging.dim_setor_orgao`
