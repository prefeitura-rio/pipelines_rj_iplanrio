{{
    config(
        alias="cnpj",
        schema="brutos_bcadastro",
        materialized="table",
        partition_by={
            "field": "cnpj_particao",
            "data_type": "int64",
            "range": {"start": 0, "end": 100000000000, "interval": 34722222},
        },
    )
}}

with
    fonte as (
        select
            _airbyte_raw_id,
            _airbyte_extracted_at,
            _airbyte_meta,
            _airbyte_generation_id,
            id,
            doc,
            key,
            seq,
            value,
            last_seq
        from {{ source("brutos_bcadastro_staging", "chcnpj_bcadastros") }}
        where timestamp_trunc(_airbyte_extracted_at, day) = timestamp("2025-03-23")
    ),

    sigla_uf_bd as (select sigla from {{ source("br_bd_diretorios_brasil", "uf") }}),

    municipio_bd as (
        select id_municipio_rf, nome as municipio_nome
        from {{ source("br_bd_diretorios_brasil", "municipio") }}
    ),

    dominio as (
        select id, descricao, column from {{ ref("dominio") }} where source = 'cnpj'
    ),



    fonte_parseada as (
        select
            -- Primary key
            nullif(json_value(doc, '$.cnpj'), '') as cnpj,

            -- Foreign keys
            nullif(json_value(doc, '$.codigoMunicipio'), '') as id_municipio,
            nullif(json_value(doc, '$.codigoPais'), '') as id_pais,
            cast(
                cast(
                    nullif(json_value(doc, '$.naturezaJuridica'), '') as int64
                ) as string
            ) as id_natureza_juridica,
            cast(
                cast(
                    nullif(json_value(doc, '$.qualificacaoResponsavel'), '') as int64
                ) as string
            ) as id_qualificacao_responsavel,
            cast(
                cast(nullif(json_value(doc, '$.porteEmpresa'), '') as int64) as string
            ) as id_porte_empresa,
            cast(
                cast(
                    nullif(json_value(doc, '$.indicadorMatriz'), '') as int64
                ) as string
            ) as id_indicador_matriz,
            nullif(
                json_value(doc, '$.tipoOrgaoRegistro'), ''
            ) as id_tipo_orgao_registro,
            cast(
                cast(nullif(json_value(doc, '$.motivoSituacao'), '') as int64) as string
            ) as id_motivo_situacao,
            cast(
                cast(
                    nullif(json_value(doc, '$.situacaoCadastral'), '') as int64
                ) as string
            ) as id_situacao_cadastral,

            -- Business data
            nullif(json_value(doc, '$.nomeEmpresarial'), '') as nome_empresarial,
            nullif(json_value(doc, '$.nomeFantasia'), '') as nome_fantasia,
            nullif(json_value(doc, '$.capitalSocial'), '') as capital_social,
            nullif(json_value(doc, '$.cnaeFiscal'), '') as cnae_fiscal,
            nullif(json_value(doc, '$.cnaeSecundarias'), '') as cnae_secundarias,
            nullif(json_value(doc, '$.nire'), '') as nire,
            nullif(json_value(doc, '$.cnpjSucedida'), '') as cnpj_sucedida,

            -- Dates
            safe.parse_date(
                '%Y%m%d', nullif(json_value(doc, '$.dataInicioAtividade'), '')
            ) as data_inicio_atividade,
            safe.parse_date(
                '%Y%m%d', nullif(json_value(doc, '$.dataSituacaoCadastral'), '')
            ) as data_situacao_cadastral,
            safe.parse_date(
                '%Y%m%d', nullif(json_value(doc, '$.dataSituacaoEspecial'), '')
            ) as data_situacao_especial,
            safe.parse_date(
                '%Y%m%d', nullif(json_value(doc, '$.dataInclusaoResponsavel'), '')
            ) as data_inclusao_responsavel,

            -- Status and demographics
            nullif(json_value(doc, '$.situacaoEspecial'), '') as situacao_especial,
            case
                when regexp_contains(json_value(doc, '$.enteFederativo'), r'^[0-9]+$')
                then
                    cast(
                        cast(
                            nullif(json_value(doc, '$.enteFederativo'), '') as int64
                        ) as string
                    )
                else upper(nullif(json_value(doc, '$.enteFederativo'), ''))
            end as id_ente_federativo,

            -- Contact
            nullif(json_value(doc, '$.dddTelefone1'), '') as ddd_telefone_1,
            nullif(json_value(doc, '$.telefone1'), '') as telefone_1,
            nullif(json_value(doc, '$.dddTelefone2'), '') as ddd_telefone_2,
            nullif(json_value(doc, '$.telefone2'), '') as telefone_2,
            nullif(json_value(doc, '$.email'), '') as email,

            -- Address
            nullif(json_value(doc, '$.cep'), '') as endereco_cep,
            nullif(json_value(doc, '$.uf'), '') as endereco_uf,
            nullif(json_value(doc, '$.bairro'), '') as endereco_bairro,
            nullif(json_value(doc, '$.tipoLogradouro'), '') as endereco_tipo_logradouro,
            nullif(json_value(doc, '$.logradouro'), '') as endereco_logradouro,
            nullif(json_value(doc, '$.numero'), '') as endereco_numero,
            nullif(json_value(doc, '$.complemento'), '') as endereco_complemento,
            nullif(
                json_value(doc, '$.nomeCidadeExterior'), ''
            ) as endereco_nome_cidade_exterior,

            -- Accountant Information
            nullif(json_value(doc, '$.tipoCrcContadorPF'), '') as tipo_crc_contador_pf,
            nullif(json_value(doc, '$.contadorPJ'), '') as contador_pj,
            nullif(
                json_value(doc, '$.classificacaoCrcContadorPF'), ''
            ) as classificacao_crc_contador_pf,
            nullif(
                json_value(doc, '$.sequencialCrcContadorPF'), ''
            ) as sequencial_crc_contador_pf,
            nullif(json_value(doc, '$.contadorPF'), '') as contador_pf,
            nullif(json_value(doc, '$.tipoCrcContadorPJ'), '') as tipo_crc_contador_pj,
            nullif(
                json_value(doc, '$.classificacaoCrcContadorPJ'), ''
            ) as classificacao_crc_contador_pj,
            nullif(json_value(doc, '$.ufCrcContadorPJ'), '') as uf_crc_contador_pj,
            nullif(json_value(doc, '$.ufCrcContadorPF'), '') as uf_crc_contador_pf,
            nullif(
                json_value(doc, '$.sequencialCrcContadorPJ'), ''
            ) as sequencial_crc_contador_pj,

            -- Responsible Person
            nullif(json_value(doc, '$.cpfResponsavel'), '') as cpf_responsavel,

            -- arrays
            json_extract_array(doc, '$.tiposUnidade') as tipos_unidade,
            json_extract_array(doc, '$.formasAtuacao') as formas_atuacao,
            json_extract_array(doc, '$.socios') as socios,
            json_extract_array(doc, '$.sucessoes') as sucessoes,

            -- Metadata
            nullif(json_value(doc, '$.timestamp'), '') as timestamp,
            nullif(json_value(doc, '$.language'), '') as language,
            nullif(
                json_value(replace(to_json_string(doc), '~', ''), '$.version'), ''
            ) as version,

            -- Outros
            id,
            key,
            nullif(json_value(value, '$.rev'), '') as rev,
            nullif(json_value(doc, '$._id'), '') as _id,
            nullif(json_value(doc, '$._rev'), '') as _rev,

            seq,
            last_seq,
            _airbyte_raw_id as airbyte_raw_id,
            _airbyte_extracted_at as airbyte_extracted_at,
            struct(
                nullif(json_value(_airbyte_meta, '$.changes'), '') as changes,
                nullif(json_value(_airbyte_meta, '$.sync_id'), '') as sync_id
            ) as airbyte_meta,
            _airbyte_generation_id as airbyte_generation_id,

        from fonte
    ),

    array_convert_tb as (
        SELECT
            cnpj,
            seq,
            version,
            ARRAY_AGG(
            DISTINCT
                tut.descricao
            ) as tipos_unidade,
            ARRAY_AGG(
            DISTINCT
                fat.descricao
            ) as formas_atuacao
        FROM fonte_parseada t,
            UNNEST(t.formas_atuacao) as fa,
            UNNEST(t.tipos_unidade) as tu
        LEFT JOIN
            (
                select id as tipos_unidade_id, descricao
                from dominio
                where column = 'tipo_unidade'
            ) tut
            on CAST(CAST(JSON_VALUE(tu) AS INT64) AS STRING) = tut.tipos_unidade_id
        LEFT JOIN
            (
                select id as formas_atuacao_id, descricao
                from dominio
                where column = 'forma_atuacao'
            ) fat
            on CAST(CAST(JSON_VALUE(fa) AS INT64) AS STRING) = fat.formas_atuacao_id
        GROUP BY 1,2,3
    ),

    fonte_intermediaria as (
        select
            -- Primary key
            t.cnpj,

            -- Foreign keys
            t.id_municipio,
            t.id_pais,
            t.id_natureza_juridica,
            t.id_qualificacao_responsavel,
            t.id_porte_empresa,
            t.id_indicador_matriz,
            t.id_tipo_orgao_registro,
            t.id_motivo_situacao,
            t.id_situacao_cadastral,

            -- Business data
            t.nome_empresarial,
            t.nome_fantasia,
            t.capital_social,
            t.cnae_fiscal,
            t.cnae_secundarias,
            t.nire,
            t.cnpj_sucedida,
            -- Dates
            t.data_inicio_atividade,
            t.data_situacao_cadastral,
            t.data_situacao_especial,
            t.data_inclusao_responsavel,

            -- Status and demographics
            t.situacao_especial,
            t.id_ente_federativo,
            case
                when id_ente_federativo = 'BR'
                then 'União'
                when regexp_contains(id_ente_federativo, r'^[0-9]+$')
                then 'Município'
                when
                    upper(id_ente_federativo)
                    in (select upper(id_ente_federativo) from sigla_uf_bd)
                then 'Estado'
                else null
            end as ente_federativo,

            -- Contact
            t.ddd_telefone_1,
            t.telefone_1,
            t.ddd_telefone_2,
            t.telefone_2,
            t.email,

            -- Address
            t.endereco_cep,
            t.endereco_uf,
            t.endereco_bairro,
            t.endereco_tipo_logradouro,
            t.endereco_logradouro,
            t.endereco_numero,
            t.endereco_complemento,
            t.endereco_nome_cidade_exterior,

            -- Accountant Information
            t.tipo_crc_contador_pf,
            t.contador_pj,
            t.classificacao_crc_contador_pf,
            t.sequencial_crc_contador_pf,
            t.contador_pf,
            t.tipo_crc_contador_pj,
            t.classificacao_crc_contador_pj,
            t.uf_crc_contador_pj,
            t.uf_crc_contador_pf,
            t.sequencial_crc_contador_pj,

            -- Responsible Person
            t.cpf_responsavel,
            -- Business arrays
            actb.tipos_unidade,
            actb.formas_atuacao,

            t.socios,
            t.sucessoes,
            -- Metadata
            t.timestamp,
            t.language,
            t.version,
            -- Outros
            t.id,
            t.key,
            t.rev,
            t._id,
            t._rev,
            t.seq,
            t.last_seq,
            t.airbyte_raw_id,
            t.airbyte_extracted_at,
            t.airbyte_meta,
            t.airbyte_generation_id,
            -- Joins
            md.municipio_nome as endereco_municipio,
            sc.descricao as situacao_cadastral,
            ms.descricao as motivo_situacao,
            org.descricao as tipo_orgao_registro,
            nj.descricao as natureza_juridica,
            pe.descricao as porte_empresa,
            im.descricao as indicador_matriz,
            qr.descricao as qualificacao_responsavel,

            cast(t.cnpj as int64) as cnpj_particao
        from fonte_parseada t
        left join array_convert_tb as actb
            on t.cnpj = actb.cnpj and t.seq = actb.seq and t.version = actb.version

        left join
            municipio_bd as md
            on cast(t.id_municipio as int64) = cast(md.id_municipio_rf as int64)
        left join
            (
                select id as id_situacao_cadastral, descricao
                from dominio
                where column = 'situacao_cadastral'
            ) sc
            on t.id_situacao_cadastral = sc.id_situacao_cadastral
        left join
            (
                select id as id_motivo_situacao, descricao
                from dominio
                where column = 'motivo_situacao_cadastral'
            )
            ms on t.id_motivo_situacao = ms.id_motivo_situacao
        left join
            (
                select id as id_tipo_orgao_registro, descricao
                from dominio
                where column = 'tipo_orgao_registro'
            )
            org on t.id_tipo_orgao_registro = org.id_tipo_orgao_registro
        left join
            (
                select id as id_natureza_juridica, descricao
                from dominio
                where column = 'natureza_juridica'
            )
            nj on t.id_natureza_juridica = nj.id_natureza_juridica
        left join
            (
                select id as id_porte_empresa, descricao
                from dominio
                where column = 'porte_empresa'
            )
            pe on t.id_porte_empresa = pe.id_porte_empresa
        left join
            (
                select id as id_indicador_matriz, descricao
                from dominio
                where column = 'indicador_matriz'
            )
            im on t.id_indicador_matriz = im.id_indicador_matriz
        left join
            (
                select id as id_qualificacao_responsavel, descricao
                from dominio
                where column = 'qualificacao_responsavel'
            )
            qr on t.id_qualificacao_responsavel = qr.id_qualificacao_responsavel
    ),

    fonte_padronizada as (
        select
            -- Primary key
            t.cnpj,

            -- Foreign keys
            t.id_municipio,
            t.id_pais,
            t.id_natureza_juridica,
            t.id_qualificacao_responsavel,
            t.id_porte_empresa,
            t.id_indicador_matriz,
            t.id_tipo_orgao_registro,
            t.id_motivo_situacao,
            t.id_situacao_cadastral,

            -- Business data
            t.nome_empresarial,
            {{ proper_br("nome_fantasia") }} as nome_fantasia,  -- Padronizado
            t.capital_social,
            t.cnae_fiscal,
            t.cnae_secundarias,
            t.nire,
            t.cnpj_sucedida,
            -- Dates
            t.data_inicio_atividade,
            t.data_situacao_cadastral,
            t.data_situacao_especial,
            t.data_inclusao_responsavel,

            -- Status and demographics
            {{ proper_br("situacao_especial") }} as situacao_especial,  -- Padronizado
            t.id_ente_federativo,
            {{ proper_br("ente_federativo") }} as ente_federativo,

            -- Contact
            t.ddd_telefone_1,
            t.telefone_1,
            t.ddd_telefone_2,
            t.telefone_2,
            t.email,

            -- Address
            t.endereco_cep,
            t.endereco_uf,
            {{ proper_br("endereco_bairro") }} as endereco_bairro,  -- Padronizado
            {{ proper_br("endereco_tipo_logradouro") }} as endereco_tipo_logradouro,  -- Padronizado
            {{ proper_br("endereco_logradouro") }} as endereco_logradouro,  -- Padronizado
            t.endereco_numero,
            {{ proper_br("endereco_complemento") }} as endereco_complemento,  -- Padronizado
            t.endereco_nome_cidade_exterior,
            t.endereco_municipio,

            -- Accountant Information
            t.tipo_crc_contador_pf,
            t.contador_pj,
            t.classificacao_crc_contador_pf,
            t.sequencial_crc_contador_pf,
            t.contador_pf,
            t.tipo_crc_contador_pj,
            t.classificacao_crc_contador_pj,
            t.uf_crc_contador_pj,
            t.uf_crc_contador_pf,
            t.sequencial_crc_contador_pj,

            -- Responsible Person
            t.cpf_responsavel,

            -- Business arrays
            t.tipos_unidade,
            t.formas_atuacao,
            t.socios,
            t.sucessoes,
            -- Metadata
            t.timestamp,
            t.language,

            -- Outros
            STRUCT(
                t.id,
                t.key,
                t.rev,
                t._id,
                t._rev,
                t.version,
                t.seq,
                t.last_seq,
                t.airbyte_raw_id,
                t.airbyte_extracted_at,
                t.airbyte_meta,
                t.airbyte_generation_id
            ) as airbyte,
            -- descricoes
            {{ proper_br("tipo_orgao_registro") }} as tipo_orgao_registro,
            {{ proper_br("motivo_situacao") }} as motivo_situacao,
            {{ proper_br("situacao_cadastral") }} as situacao_cadastral,
            {{ proper_br("natureza_juridica") }} as natureza_juridica,
            {{ proper_br("porte_empresa") }} as porte_empresa,
            {{ proper_br("indicador_matriz") }} as indicador_matriz,
            {{ proper_br("qualificacao_responsavel") }} as qualificacao_responsavel,
            -- Partition and Rank
            t.cnpj_particao
        from fonte_intermediaria t
    ),

    fonte_deduplicada as (
        select *
        from fonte_padronizada
        qualify row_number() over (partition by cnpj order by data_situacao_cadastral desc) = 1
    ),

    final as (
        select
            -- Primary key
            cnpj,

            -- Foreign keys
            id_municipio,
            id_pais,
            id_natureza_juridica,
            id_qualificacao_responsavel,
            id_porte_empresa,
            id_indicador_matriz,
            id_tipo_orgao_registro,
            id_motivo_situacao,
            id_situacao_cadastral,

            -- Business data
            nome_empresarial,
            nome_fantasia,
            capital_social,
            cnae_fiscal,
            cnae_secundarias,
            nire,
            cnpj_sucedida,
            tipo_orgao_registro,
            porte_empresa,
            indicador_matriz,


            -- Dates
            data_inicio_atividade,
            data_situacao_cadastral,
            data_situacao_especial,
            data_inclusao_responsavel,

            -- Status and demographics
            situacao_cadastral,
            natureza_juridica,
            situacao_especial,
            motivo_situacao,
            id_ente_federativo,
            ente_federativo,

            -- Contact
            ddd_telefone_1,
            telefone_1,
            ddd_telefone_2,
            telefone_2,
            email,

            -- Address
            endereco_uf,
            endereco_cep,
            endereco_municipio,
            endereco_bairro,
            endereco_tipo_logradouro,
            endereco_logradouro,
            endereco_numero,
            endereco_complemento,
            endereco_nome_cidade_exterior,

            -- Accountant Information
            tipo_crc_contador_pf,
            contador_pj,
            classificacao_crc_contador_pf,
            sequencial_crc_contador_pf,
            contador_pf,
            tipo_crc_contador_pj,
            classificacao_crc_contador_pj,
            uf_crc_contador_pj,
            uf_crc_contador_pf,
            sequencial_crc_contador_pj,

            -- Responsible Person
            cpf_responsavel,
            qualificacao_responsavel,

            -- Business arrays
            tipos_unidade,
            formas_atuacao,
            socios,
            sucessoes,

            -- Metadata
            timestamp,
            language,

            -- Outros
            airbyte,

            -- Partition
            cnpj_particao
        from fonte_deduplicada
    )

select *
from final
