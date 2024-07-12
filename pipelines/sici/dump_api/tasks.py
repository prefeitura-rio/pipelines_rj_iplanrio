from pipelines.sici.dump_api.utils import xml_to_dataframe
from prefect import task
from prefeitura_rio.pipelines_utils.logging import log
from prefeitura_rio.pipelines_utils.infisical import get_secret
from zeep import Client, Fault, TransportError, XMLSyntaxError

@task
def get_data_from_api_soap_sici(
    wsdl: str = "http://sici.rio.rj.gov.br/Servico/WebServiceSICI.asmx?wsdl",
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

        # Call the service
        response = client.service.Get_Arvore_UA(**params)

        # Transform to df
        df = xml_to_dataframe(response)

        log(f"Data was successfully retrieved from the SICI API. DataFrame shape: {df.shape}")
        log(f"Data sample: {df.head(5)}")

        # Safe the dataframe to a CSV file
        df.to_csv("sici_data.csv", index=False)

        # Return the dataframe and the true path of the csv file
        return df, "sici_data.csv"

    except Fault as e:
        log.error(f"SOAP Fault occurred: {e}")
        raise
    except TransportError as e:
        log.error(f"Transport error occurred: {e}")
        raise
    except XMLSyntaxError as e:
        log.error(f"XML syntax error occurred: {e}")
        raise
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        raise

@task
def get_sici_api_credentials():
    """
    Get the credentials for the SICI API.
    """
    try:
        consumidor = get_secret(
            secret_name = "CONSUMIDOR",
            environment = "Production",
            path= "/api-sici",
        )
    except Exception as e:
        log.error(f"An error occurred while fetching the SICI API credentials for consumidor: {e}")
        raise

    try:
        chave_acesso = get_secret(
            secret_name="CHAVE_ACESSO",
            environment="Production",
            path="/api-sici",
        )
    except Exception as e:
        log.error(f"An error occurred while fetching the SICI API credentials for chave_acesso: {e}")
        raise

    return {
        "Codigo_UA": "",
        "Nivel": "",
        "Tipo_Arvore": "",
        "consumidor": consumidor,
        "chaveAcesso": chave_acesso,
   }