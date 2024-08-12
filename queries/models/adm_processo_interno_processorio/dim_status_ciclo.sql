SELECT
    CAST(idstatus_ciclo AS INT64) AS idstatus_ciclo,
    CAST(nome_status_ciclo AS STRING) AS nome_status_ciclo
FROM
    `rj-iplanrio.adm_processo_interno_processorio_staging.dim_status_ciclo`
