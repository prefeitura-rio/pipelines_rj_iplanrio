import pandas as pd


def xml_to_dataframe(xml: object) -> pd.DataFrame:
    """
    This function receives an XML object and returns a DataFrame.
    """
    # Parse the XML string
    root = xml

    # Extract the data
    data = []
    columns = [element.tag for element in root[0]]

    for table in root:
        row = {element.tag: element.text for element in table}
        data.append(row)

    # Create the DataFrame
    df = pd.DataFrame(data, columns=columns)

    return df
