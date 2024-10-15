SELECT
    SAFE_CAST(ID_AtvProcesso AS STRING) AS ID_AtvProcesso,
    SAFE_CAST(DSC_AtvProcesso AS STRING) AS DSC_AtvProcesso,
    SAFE_CAST(DSC_RespAtividade AS STRING) AS DSC_RespAtividade,
    SAFE_CAST(DSC_RefAtividade AS STRING) AS DSC_RefAtividade

FROM `rj-iplanrio.alvaras_staging.tab_atvprocesso`