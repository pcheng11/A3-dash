import json
import boto3
import requests
import config
import pandas as pd


dynamo_client = boto3.client('dynamodb', region_name='us-east-1')
def get_countrys_data_dash():
    response = dynamo_client.batch_get_item(
        RequestItems={
            'covid19Table': {
                'Keys': [
                    {
                        'country': {'S': 'USA'},
                    },
                    {
                        'country': {'S': 'Spain'},
                    },
                    {
                        'country': {'S': 'Italy'},
                    },
                    {
                        'country': {'S': 'France'},
                    },
                    {
                        'country': {'S': 'Germany'},
                    },
                    {
                        'country': {'S': 'UK'},
                    },
                    {
                        'country': {'S': 'China'},
                    },
                    {
                        'country': {'S': 'Iran'},
                    }
                ],
            "ProjectionExpression":"country, cases, deaths, recovered"
            }
        }
    )

    countries_label = []
    cases = []
    recovered = []
    deaths = []
    for item in response['Responses']['covid19Table']:
        countries_label.append(item['country']['S'])
        cases.append(int(item['cases']['N']))
        recovered.append(int(item['recovered']['N']))
        deaths.append(int(item['deaths']['N']))

    # get rest of the world api
    response = requests.get(config.GLOBAL_STAT_URL)
    global_data = json.loads(response.content)

    # rest of the world data
    countries_label.append("Rest of the World")
    cases.append(global_data['cases'] - sum(cases))
    recovered.append(global_data['recovered'] - sum(recovered))
    deaths.append(global_data['deaths'] - sum(deaths))
    return countries_label, cases, recovered, deaths

def get_countrys_data_map():
    response = dynamo_client.scan(TableName='covid19Table')
    country_col = []
    cases_col = []
    recovered_col = []
    deaths_col = []
    lat = []
    long = []
    for item in response['Items']:
        if 'lat' not in item:
            continue
        country_col.append(item['country']['S'])
        cases_col.append(int(item['cases']['N']))
        recovered_col.append(int(item['recovered']['N']))
        deaths_col.append(int(item['deaths']['N']))
        lat.append(float(item['lat']['N']))
        long.append(float(item['long']['N']))

    data = {
        'country': country_col,
        'cases': cases_col,
        'recovered': recovered_col,
        'deaths': deaths_col,
        'lat': lat,
        'long': long
    }
    df = pd.DataFrame(data=data)
    return df

def get_table_data():
    response = dynamo_client.scan(TableName='covid19Table')
    country_col = []
    cases_col = []
    recovered_col = []
    deaths_col = []
    for item in response['Items']:
        if 'lat' not in item:
            continue
        country_col.append(item['country']['S'])
        cases_col.append(int(item['cases']['N']))
        recovered_col.append(int(item['recovered']['N']))
        deaths_col.append(int(item['deaths']['N']))

    data = {
        'Country': country_col,
        'Cases': cases_col,
        'Recovered': recovered_col,
        'Deaths': deaths_col,
    }
    df = pd.DataFrame(data=data)
    df.sort_values('Cases', ascending=False, inplace=True)
    df = df.reset_index()
    print(df)

    return df

def get_time_line(country):
    response = dynamo_client.get_item(
        TableName='covid19Table-Calendar',
        Key={
            'country': {
                "S": country
            }
        }
    )
    data = response['Item']['data']['S'].replace("'", '"')
    data = json.loads(data)

    df = pd.DataFrame(data=data)
    return df


def get_country_data(country):
    print(country)
    response = dynamo_client.get_item(
        TableName='covid19Table',
        Key={
            'country': {
                "S": country
        }})
    return response['Item']


def name_diff_table_2_timeline(name):
    if name == 'USA':
        return 'US'
    if name == 'S. Korea':
        return "Korea, South"
    if name == 'UK':
        return "United Kingdom"
    else:
        return name


def name_diff_timeline_2_table(name):
    if name == 'US':
        return 'USA'
    if name == "Korea, South":
        return "S. Korea"
    if name == 'United Kingdom':
        return "UK"
    else:
        return name