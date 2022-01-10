import hashlib
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import sys
import os
from dotenv import load_dotenv
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'..', '.env'))


if __name__ == '__main__':
    sys.exit()

def get_data(query: str) -> list:
    """Pulls demographic data from the PMI 100k cohort."""
    pmi_conn_str = os.environ.get('PMI_CONN_STR')
    pmi_engine = create_engine(pmi_conn_str)
    # From DB
    with pmi_engine.connect() as c:
        resultproxy = c.execute(query)            

    df_dict = [
        {column: value for column, value in rowproxy.items()}
        for rowproxy in resultproxy
    ]
    print(df_dict)
    return df_dict
    
def format_data(data: list) -> dict:
    """Takes in data (dict format) and formats into the required structure."""
    out_data = []
    for d in data:
        if d['identifier_value'] in [x['identifier_value'] for x in out_data]:
            for existing_d in out_data:
                if existing_d['identifier_value'] == d['identifier_value']:
                    existing_d[d['concept_code']] = d['val']
        else:
            temp = {}
            temp['identifier_value'] = d['identifier_value'] 
            temp[d['concept_code']] = d['val']
            out_data.append(temp)

    return out_data

def format_date_of_birth(data: list) -> dict:
    """Formats dob in the data dictionary."""
    for item in data:
        dob = datetime.strptime(item['date_of_birth'], '%Y-%m-%d 00:00:00')
        new_dob = dob.strftime('%Y%m%d')
        item['dob'] = new_dob
        del item['date_of_birth']
    return data

def filter_data(data: list) -> list:
    """Filters our participants with missing dob or nhs_num."""
    return [x for x in data if len(list(x.keys())) == 3]

        

def generate_hash(data: list, salt: str) -> list:
    """
    Takes in a dict and returns a hashed column.
    Assume dict has the following columns:
    - nhs_number
    - dob (format YYYYMMDD)
    - sex
    """
    hash_store = {}
    for row in data:
        part_1 = str(hashlib.md5(row['nhs_number'].encode('utf-8')).hexdigest())
        hash_store[row['identifier_value']] = hashlib.md5((part_1 + '_' + row['dob'] + salt).encode('utf-8'))
    return [x.hexdigest() for x in hash_store.values()]

def write_to_txt(data: list, fname: str) -> None:
    """Takes in a list and writes out to text file."""

    # Write hashes to txt file
    txtfile = open(fname, 'w')
    for h in data:
        txtfile.write(str(h) + "\n")
    txtfile.close()


    




    

