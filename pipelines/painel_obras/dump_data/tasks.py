# -*- coding: utf-8 -*-
from time import sleep

from basedosdados.upload.base import Base
from google.cloud import bigquery
from prefect import task
from prefeitura_rio.pipelines_utils.gcs import list_blobs_with_prefix
from prefeitura_rio.pipelines_utils.logging import log


@task
def download_data_to_gcs(  # pylint: disable=R0912,R0913,R0914,R0915
    dataset_id: str,
    table_id: str,
    query: str,
    bd_project_mode: str = "prod",
    billing_project_id: str = None,
    location: str = "US",
):
    """
    Get data from BigQuery.
    """
    # Asserts that dataset_id and table_id are provided
    if not dataset_id or not table_id:
        raise ValueError("dataset_id and table_id must be provided")

    # If query is not a string, raise an error
    if not isinstance(query, str):
        raise ValueError("query must be a string")
    log(f"Query was provided: {query}")

    # Get billing project ID
    if not billing_project_id:
        log("Billing project ID was not provided, trying to get it from environment variable")
        try:
            bd_base = Base()
            billing_project_id = bd_base.config["gcloud-projects"][bd_project_mode]["name"]
        except KeyError:
            pass
        if not billing_project_id:
            raise ValueError(
                "billing_project_id must be either provided or inferred from environment variables"
            )
        log(f"Billing project ID was inferred from environment variables: {billing_project_id}")

    # Get data
    log("Querying data from BigQuery")
    bq_client = bigquery.Client(
        credentials=Base()._load_credentials(mode="prod"),
        project=billing_project_id,
    )
    job = bq_client.query(query)
    while not job.done():
        sleep(1)
    dest_table = job._properties["configuration"]["query"]["destinationTable"]
    dest_project_id = dest_table["projectId"]
    dest_dataset_id = dest_table["datasetId"]
    dest_table_id = dest_table["tableId"]
    log(f"Query results were stored in {dest_project_id}.{dest_dataset_id}.{dest_table_id}")

    blob_path = f"gs://datario/share/{dataset_id}/{table_id}/data.csv.gz"
    log(f"Loading data to {blob_path}")
    dataset_ref = bigquery.DatasetReference(dest_project_id, dest_dataset_id)
    table_ref = dataset_ref.table(dest_table_id)
    job_config = bigquery.job.ExtractJobConfig(compression="GZIP")
    extract_job = bq_client.extract_table(
        table_ref,
        blob_path,
        location=location,
        job_config=job_config,
    )
    extract_job.result()
    log("Data was loaded successfully")

    # Get the BLOB we've just created and make it public
    blobs = list_blobs_with_prefix("datario", f"share/{dataset_id}/{table_id}/")
    if not blobs:
        raise ValueError(f"No blob found at {blob_path}")
    for blob in blobs:
        log(f"Blob found at {blob.name}")
        blob.make_public()
        log("Blob was made public")
