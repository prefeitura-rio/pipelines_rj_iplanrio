SELECT
    CAST(idtipo_evento AS INT64) AS idtipo_evento,
    CAST(nome_evento AS STRING) AS nome_evento,
    CAST(idgrupo_evento AS INT64) AS idgrupo_evento,
    CAST(nome_grupo_evento AS STRING) AS nome_grupo_evento
FROM
    `rj-iplanrio.adm_processo_interno_processorio_staging.dim_tipo_evento`
