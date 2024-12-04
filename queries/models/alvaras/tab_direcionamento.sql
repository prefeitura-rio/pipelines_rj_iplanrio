SELECT
    SAFE_CAST(ID_Direcionamento AS STRING) AS ID_Direcionamento,
    SAFE_CAST(DSC_Direcionamento AS STRING) AS DSC_Direcionamento

FROM `rj-iplanrio.alvaras_staging.tab_direcionamento`