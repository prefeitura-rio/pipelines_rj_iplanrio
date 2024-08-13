SELECT
    CAST(ROUND(CAST(idacao AS FLOAT64)) AS INT64) AS idacao,
    CAST(ROUND(CAST(idstatus_ciclo AS FLOAT64)) AS INT64) AS idstatus_ciclo,
    CAST(ROUND(CAST(idtipo_evento AS FLOAT64)) AS INT64) AS idtipo_evento,
    CAST(ROUND(CAST(iddocumento AS FLOAT64)) AS INT64) AS iddocumento,
    CAST(ROUND(CAST(idsetor AS FLOAT64)) AS INT64) AS idsetor,
    CAST(ROUND(CAST(iddata_inicio AS FLOAT64)) AS INT64) AS iddata_inicio,
    CAST(ROUND(CAST(iddata_fim AS FLOAT64)) AS INT64) AS iddata_fim,
    CAST(hora_registro_inicio AS TIME) AS hora_registro_inicio,
    CAST(hora_registro_fim AS TIME) AS hora_registro_fim,
    CAST(ROUND(CAST(iddata_inicio_ciclo AS FLOAT64)) AS INT64) AS iddata_inicio_ciclo,
    CAST(ROUND(CAST(iddata_fim_ciclo AS FLOAT64)) AS INT64) AS iddata_fim_ciclo,
    CAST(data_hora_carga AS TIMESTAMP) AS data_hora_carga
FROM
    `rj-iplanrio.adm_processo_interno_processorio_staging.fato_tramitacao_documento`
