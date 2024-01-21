# Scrapes the yearly ranking data from SCCA's points report html tables 
#
# Created by Braeden Richards
# GitHub: bjrichards

# Imports
import bs4
import requests
import pandas
import sys
from io import StringIO

# Supporting functions
def create_full_url_from_year(year: int, url: str) -> str:
    result: str = ""
    result = url + str(year)
    return result

def is_integer(n: any):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def retrieve_site(url: str):
    # Set request to look like it came from the chrome broswer
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
    result = requests.get(url=url, headers=headers)
    
    return result



# Main script
if __name__ == "__main__":
    BASE_URL: str = 'https://www.crbscca.com/staffAdmin/points/pointsReports/nationwideReportAllClasses.php?theYear='

    # Create URL for data grab, check if valid url
    full_url: str = create_full_url_from_year(2023, BASE_URL)
    if not full_url:
        print("Error, url not properly created.")
        sys.exit()
    
    # Retrieve data from site
    site_response: requests.Response = retrieve_site(url=full_url)
    if not site_response.ok:
        print("Error when retrieving site data.")
        sys.exit()
    
    # Massage data into proper table format
    df_list: list[pandas.DataFrame] = pandas.read_html(StringIO(site_response.text), header=0)
    # Grab only first real (not first in general) table for now
    table_1_df = df_list[1]
    # Remove empty final columns (from bad read in of html)
    table_1_df_minus_columns: pandas.DataFrame = table_1_df.drop(columns=table_1_df.columns[27:])
    # Remove end row of table when it is not data from table (cleaning)
    if not is_integer(table_1_df_minus_columns.iloc[-1,0]):
        table_1_df_minus_columns = table_1_df_minus_columns.head(-1)
    # Insert the year of the data into first column
    table_1_df_minus_columns.insert(0, 'year', '2023')
    # Output table to csv
    table_1_df_minus_columns.to_csv('./test_output_non-ipynb.csv')