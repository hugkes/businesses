import time
import requests
import pandas as pd

def make_request(api_key, location, **kwargs):
    
    '''
    Makes a request to Place Details API
    Returns:
        Dataframe with up to 60 results
    Parameters:
        api_key (str): API key defined with Google Account
        location (str): Latitude and longitude values for centre of search
        radius (int): Meters around location to search
        typ (str): Filter by category of the places to return, e.g. 'cafe'
        rankby (str): alternative to radius - rankby distance not prominence (default)
    '''
    
    # Constants
    typ = kwargs.get('typ', None)
    radius = kwargs.get('radius', None)
    rankby = kwargs.get('rankby', None)
    
    # Admin Params - keep empty as we are using GET method
    PAYLOAD = {}
    HEADERS = {}
    # Keep output_type as json
    OUTPUT_TYPE = 'json'
    
    # Define empty dataframes
    df = pd.DataFrame()
    df_2 = pd.DataFrame()
    df_3 = pd.DataFrame()
    
    # Define URL for API call
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/{OUTPUT_TYPE}?location={location}&radius={radius}&type={typ}&rankby={rankby}&key={api_key}'
    
    # Get first page of response
    response = requests.request('GET', url, headers=HEADERS, data=PAYLOAD)
    
    # Save into a dataframe
    json = response.json()
    df = pd.DataFrame(json['results'])
    
    # See if there is a next page of 20 results
    if 'next_page_token' in json.keys():
        
        # Wait 2 seconds to allow Google to validate next_page_token
        time.sleep(2)
        
        page_token = json['next_page_token']
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/{OUTPUT_TYPE}?location={location}&radius={radius}&type={typ}&rankby={rankby}&pagetoken={page_token}&key={api_key}'
        
        response = requests.request('GET', url, headers=HEADERS, data=PAYLOAD)
        
        json = response.json()
        df_2 = pd.DataFrame(json['results'])
        
        if 'next_page_token' in json.keys():
            
            time.sleep(2)
        
            page_token = json['next_page_token']
            url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/{OUTPUT_TYPE}?location={location}&radius={radius}&type={typ}&rankby={rankby}&pagetoken={page_token}&key={api_key}'

            response = requests.request('GET', url, headers=HEADERS, data=PAYLOAD)

            json = response.json()
            df_3 = pd.DataFrame(json['results'])
    
    # Join all dataframes and return result
    all_df = pd.concat([df, df_2, df_3])
    
    return all_df