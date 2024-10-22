from prefect import task
from prefeitura_rio.pipelines_utils.infisical import get_secret
from prefeitura_rio.pipelines_utils.logging import log
from zeep import Client

from pipelines.sici.dump_api.utils import xml_to_dataframe


@task
def get_data_from_api_soap_sici(
    wsdl: str = "http://sici.rio.rj.gov.br/Servico/WebServiceSICI.asmx?wsdl",
    endpoint: str = "Get_Arvore_UA",
    params: dict = {
        "Codigo_UA": "",
        "Nivel": "",
        "Tipo_Arvore": "",
        "consumidor": "",
        "chaveAcesso": "",
    },
):
    """
    Get data from the SICI API.
    """
    try:
        # Create a client
        client = Client(wsdl=wsdl)

        log(f"Calling the SICI API with the following parameters: {params}")
        log(type(params))

        if endpoint == "Get_Arvore_UA":
            # Call the service
            response = client.service.Get_Arvore_UA(**params)
        elif endpoint == "Get_UG_Tipo_UG":
            response = client.service.Get_UG_Tipo_UG(**params)
        else:
            raise ValueError(f"Invalid endpoint: {endpoint}")

        # Transform to df
        df = xml_to_dataframe(response)

        log(f"Data was successfully retrieved from the SICI API. DataFrame shape: {df.shape}")
        log(f"Data sample: {df.head(5)}")

        # Safe the dataframe to a CSV file
        if endpoint == "Get_Arvore_UA":
            df.to_csv("sici_data.csv", index=False)
            # Return the true path of the csv file
            return "sici_data.csv"
        if endpoint == "Get_UG_Tipo_UG":
            df.to_csv("sici_data_ug.csv", index=False)
            return "sici_data_ug.csv"
        raise ValueError(f"Invalid endpoint: {endpoint}")

    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        raise


@task
def get_sici_api_credentials(
    endpoint_parameters: dict = {
        "Codigo_UA": "",
        "Nivel": "",
        "Tipo_Arvore": "",
    },
):
    """
    Get the credentials for the SICI API.
    """
    try:
        consumidor = get_secret(
            secret_name="CONSUMIDOR",
            # environment = "Production",
            path="/api-sici",
        )
    except Exception as e:
        log.error(f"An error occurred while fetching the SICI API credentials for consumidor: {e}")
        raise

    try:
        chave_acesso = get_secret(
            secret_name="CHAVE_ACESSO",
            # environment="Production",
            path="/api-sici",
        )
    except Exception as e:
        log.error(
            f"An error occurred while fetching the SICI API credentials for chave_acesso: {e}",
        )
        raise

    # Create an all_parameters dict with the consumidor and chave_acesso and the endpoint_parameters
    all_parameters = {
        "consumidor": consumidor,
        "chaveAcesso": chave_acesso,
        **endpoint_parameters,
    }

    log(f"Credentials for the SICI API were successfully retrieved: {all_parameters}")
    log(f"Endpoint parameters: {endpoint_parameters}")
    log(type(all_parameters))

    return all_parameters
