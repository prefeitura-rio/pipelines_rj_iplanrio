SELECT
    SAFE_CAST(ID_TipoSolicitacao AS STRING) AS ID_TipoSolicitacao,
    SAFE_CAST(DSC_TipoSolicitacao AS STRING) AS DSC_TipoSolicitacao

FROM `rj-iplanrio.alvaras_staging.tab_tiposolicitacao`