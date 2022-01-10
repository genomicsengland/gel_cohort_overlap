from utils import utils
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import text


LOGGER = logging.getLogger(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

def main():
    # Get data from PMI
    LOGGER.info('Getting demographic data from the PMI and formatting to required structure')

    query = text(open('sql/pmi_demographics.sql').read())

    pmi_data = utils.filter_data(utils.format_data(utils.get_data(query)))

    hash_input_data = utils.format_date_of_birth(pmi_data)    

    LOGGER.info('Generating MD5 hashes for the raw_data')
    hashes = utils.generate_hash(hash_input_data, os.environ.get('SALT'))

    LOGGER.info('Writing out to text file')
    fpath = 'data/' + 'GEL_MD5_' + datetime.today().strftime('%Y%m%d') 
    utils.write_to_txt(hashes, fpath)

if __name__ == '__main__':
    main()


