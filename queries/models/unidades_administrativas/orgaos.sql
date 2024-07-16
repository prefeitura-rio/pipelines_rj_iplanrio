SELECT 
  SAFE_CAST(
    REGEXP_REPLACE(cd_ua, r'\.0$', '') AS STRING
  ) id_unidade_administrativa,
  SAFE_CAST(
    REGEXP_REPLACE(sigla_ua, r'\.0$', '') AS STRING
  ) sigla_unidade_administrativa,
  SAFE_CAST(
    REGEXP_REPLACE(nome_ua, r'\.0$', '') AS STRING
  ) nome_unidade_administrativa,
  SAFE_CAST(
    REGEXP_REPLACE(cd_ua_pai, r'\.0$', '') AS STRING
  ) id_unidade_administrativa_pai,
  SAFE_CAST(
    REGEXP_REPLACE(cd_ua_pai, r'\.0$', '') AS STRING
  ) id_unidade_administrativa_pai,
  SAFE_CAST(
    REGEXP_REPLACE(nivel, r'\.0$', '') AS STRING
  ) nivel,
  SAFE_CAST(
    REGEXP_REPLACE(ordem_ua_basica, r'\.0$', '') AS STRING
  ) ordem_unidade_administrativa_basica,
  SAFE_CAST(
    REGEXP_REPLACE(ordem_absoluta, r'\.0$', '') AS STRING
  ) ordem_absoluta,
  SAFE_CAST(
    REGEXP_REPLACE(ordem_relativa, r'\.0$', '') AS STRING
  ) ordem_relativa
FROM `rj-iplanrio.unidades_administrativas_staging.orgaos`