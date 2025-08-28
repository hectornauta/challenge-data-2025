import pandas as pd
from db import get_connection
from typing import Optional, Dict


def etl_tables():
    base_path = 'data/'
    # Hacemos un diccionario de la fconfiguración de cada archivo, con Int64 porque tiene nulos
    dict_files = {
        'departments': {
            'csv_file': base_path + 'departments.csv',
            'columns': {
                'id': 'Int64',
                'name': str
            }
        },
        'hired_employees': {
            'csv_file': base_path + 'hired_employees.csv',
            'columns': {
                'id': 'Int64',
                'name': str,
                'datetime': str,
                'department_id': 'Int64',
                'job_id': 'Int64'
            }
        },
        'jobs': {
            'csv_file': base_path + 'jobs.csv',
            'columns': {
                'id': 'Int64',
                'name': str
            }
        }
    }
    # Recorremos el diccionario
    for entity_name, entity_config in dict_files.items():
        process_entity(entity_name, entity_config)
        

def process_entity(entity_name: str, entity_config: Dict):
    # Armamos la ruta completa
    filepath = entity_config['csv_file']
    try:
        dataframe = pd.read_csv(
            filepath,
            delimiter=',',
            dtype=entity_config['columns'],
            names=list(entity_config['columns'].keys())
        )
    except FileNotFoundError:
        raise Exception(f'El archivo {filepath} no existe')
    # Cambiamos a datetime
    if entity_name == 'hired_employees':
        dataframe['datetime'] = pd.to_datetime(dataframe['datetime'], format='ISO8601')
    # Guardamos a la base de datos
    conn = get_connection()
    dataframe.to_sql(
        entity_name,
        conn,
        if_exists='replace',
        index=False
    )
    conn.close()

etl_tables()