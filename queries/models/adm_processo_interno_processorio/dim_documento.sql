SELECT
    CAST(iddocumento AS INT64) AS iddocumento,
    CAST(numero_documento AS STRING) AS numero_documento,
    CAST(idclassificacao AS INT64) AS idclassificacao,
    CAST(nome_classificacao AS STRING) AS nome_classificacao,
    CAST(codigo_classificacao AS STRING) AS codigo_classificacao,
    CAST(idsubclasse AS INT64) AS idsubclasse,
    CAST(nome_subclasse AS STRING) AS nome_subclasse,
    CAST(idclasse AS INT64) AS idclasse,
    CAST(nome_classe AS STRING) AS nome_classe,
    CAST(idassunto AS INT64) AS idassunto,
    CAST(nome_assunto AS STRING) AS nome_assunto,
    CAST(idforma_documento AS INT64) AS idforma_documento,
    CAST(nome_forma_documento AS STRING) AS nome_forma_documento,
    CAST(idtipo_forma_documento AS INT64) AS idtipo_forma_documento,
    CAST(nome_tipo_forma_documento AS STRING) AS nome_tipo_forma_documento
FROM
    `rj-iplanrio.adm_processo_interno_processorio_staging.dim_documento`
