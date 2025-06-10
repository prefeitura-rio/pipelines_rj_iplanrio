# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union

import geopandas as gpd
import pandas as pd
import requests
from prefect import task
from prefeitura_rio.pipelines_utils.logging import log


@task
def download_equipamentos_from_datario(
    url: str = "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Educacao/SME/MapServer/1",
    path: Union[str, Path] = "/tmp/escolas_geo/",
    crs: str = None,
) -> Path:
    """
    Baixa dados de equipamentos municipais do Rio de Janeiro de um serviço ArcGIS REST,
    Cria o GeoDataFrame e salva os dados em um arquivo CSV.
    Parameters:
        - url: URL do serviço ArcGIS REST.
        - path: Caminho onde os dados serão salvos.
        - crs: Sistema de referência de coordenadas (CRS) original dos dados.
    Returns:
        - path: Caminho para o diretório onde os dados foram salvos.
    """
    url = url[:-1] if url.endswith("/") else url
    url = url + "/query" if not url.endswith("/query") else url

    log(f"Using url:\n{url}")

    params = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "f": "json",
    }
    offset = 0
    all_features = []

    log("Iniciando o download...")
    pages = 0
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
        pages += 1
        log(f"Página {pages} baixada com {len(features)} registros.")
        if not data.get("exceededTransferLimit", False):
            break

    if not all_features:
        log("Nenhum dado de escola foi encontrado.")
        return None

    log(
        f"Download completo!\nTotal de {pages} páginas.\nTotal de {len(all_features)} rows."
    )

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
        crs=crs,  # Define o CRS original (UTM)
    )

    log(f"Convertendo coordenadas para de {crs} para EPSG:4326 (Lat/Lon)...")
    # Converte o GeoDataFrame para o sistema de coordenadas geográficas padrão
    dataframe = dataframe.to_crs("EPSG:4326")
    dataframe["latitude"] = dataframe.geometry.y
    dataframe["longitude"] = dataframe.geometry.x
    log("Processo concluído!")

    log(f"Dataframe:\n{dataframe.head()}")

    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path / "data.csv", index=False)
    log(f"Dados salvos em {path}/")

    return path
