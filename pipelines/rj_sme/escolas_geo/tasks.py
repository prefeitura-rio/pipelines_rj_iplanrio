# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union

import geopandas as gpd
import pandas as pd
import requests
from prefeitura_rio.pipelines_utils.logging import log


def download_and_dump_escolas_geo(
    url: str = "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Educacao/SME/MapServer/1/query",
    path: Union[str, Path] = "/tmp/escolas_geo/",
) -> Path:
    """
    Baixa todos os dados de escolas municipais do Rio de Janeiro de um serviço ArcGIS REST,
    cria um GeoDataFrame com as coordenadas corretas e o retorna.
    """
    params = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "f": "json",
    }
    offset = 0
    all_features = []

    log("Iniciando o download dos dados das escolas...")
    while True:
        params["resultOffset"] = offset
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            log(f"Erro ao conectar com o servidor: {e}")
            return None

        features = data.get("features", [])
        if not features:
            log("Busca finalizada.")
            break

        all_features.extend(features)
        offset += len(features)

        if not data.get("exceededTransferLimit", False):
            break

    if not all_features:
        log("Nenhum dado de escola foi encontrado.")
        return None

    log(f"\nDownload completo! Total de {len(all_features)} escolas encontradas.")
    log("Processando dados e criando GeoDataFrame...")

    processed_data = []
    for feature in all_features:
        attributes = feature.get("attributes", {})
        geometry = feature.get("geometry", {})
        if geometry:
            attributes["longitude"] = geometry.get("x")
            attributes["latitude"] = geometry.get("y")
        processed_data.append(attributes)

    dataframe = pd.DataFrame(processed_data)

    # --- CORREÇÃO APLICADA AQUI ---
    # Cria o GeoDataFrame na ordem correta: (x=longitude, y=latitude)
    dataframe = gpd.GeoDataFrame(
        dataframe,
        geometry=gpd.points_from_xy(dataframe.longitude, dataframe.latitude),
        crs="EPSG:31983",  # Define o CRS original (UTM)
    )

    log("Convertendo coordenadas para WGS 84 (Lat/Lon)...")
    # Converte o GeoDataFrame para o sistema de coordenadas geográficas padrão
    dataframe = dataframe.to_crs("EPSG:4326")
    dataframe["latitude"] = dataframe.geometry.y
    dataframe["longitude"] = dataframe.geometry.x

    # dataframe["tipo_denominacao"] = dataframe["denominacao"].apply(
    #     lambda x: x.split(" - ")[0]
    # )
    # dataframe["nome_denominacao"] = dataframe["denominacao"].apply(
    #     lambda x: x.split(" - ")[1] if len(x.split(" - ")) == 2 else x
    # )

    # l = []
    # for tipo, den in zip(
    #     dataframe["tipo"].tolist(), dataframe["tipo_denominacao"].tolist()
    # ):
    #     l.append(
    #         den.replace(tipo, "")
    #         .strip()
    #         .replace("de ", "")
    #         .replace("do ", "")
    #         .replace("da ", "")
    #     )
    # dataframe["tipo_denominacao"] = l

    dataframe["cre"] = dataframe["cre"].astype(int).apply(lambda x: str(x) if len(str(x)) >= 2 else f"0{x}")
    rename_cols = {
        # "objectid": "objectid",
        "cre": "cre",
        "designacao": "designacao",
        "tipo": "tipo",
        "denominacao": "nome",
        "latitude": "latitude",
        "longitude": "longitude",
        "geometry": "geometry",
        # "tipo_denominacao": "tipo_denominacao",
        # "nome_denominacao": "nome_denominacao",
    }
    dataframe = dataframe.rename(columns=rename_cols).reset_index(drop=True)
    dataframe = dataframe[list(rename_cols.values())]
    log("Processo concluído!")

    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path / "data.csv", index=False)
    log(f"Dados salvos em {path}/")

    return path
