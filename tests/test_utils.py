import logging
import pytest
from sqlalchemy import create_engine
import csv
from utils import utils
import hashlib
import pathlib

class TestHashUtils:

    @pytest.fixture()
    def target_data(self):        
        gel_id = 1
        cpath = str(pathlib.Path(__file__).parent.resolve())
        test_path = cpath + '/setup/gel.txt'
        with open(test_path) as f:
            test_reader = csv.reader(f, delimiter='\t')
            test_data = []
            for data in test_reader:
                temp_dict = {}
                temp_dict['nhs_number'] = data[0]
                temp_dict['nhs_number_hash'] = data[1]
                temp_dict['dob'] = data[3]
                temp_dict['hash'] = data[4]
                temp_dict['identifier_value'] = gel_id
                gel_id += 1
                test_data.append(temp_dict)

        return test_data

    @pytest.fixture()
    def pmi_sample_data(self):
        return [
            {
                'identifier_value' : 1,
                'val':'1900-01-01 00:00:00',
                'concept_code':'date_of_birth'
            },
            {
                'identifier_value' : 1,
                'val':'000000000',
                'concept_code':'nhs_number'
            },
            {
                'identifier_value' : 2,
                'val':'000000001',
                'concept_code':'nhs_number'
            }
        ]


    def test_format_data(self, pmi_sample_data):
        """Takes in a list of dictionaries in the following format
            [{'identifier_value': x, 'val':val_x1, 'concept_code':code_x1}]

        and returns a list of dictionaries in the following format
        data = input_daddta

            [{'identifier_value': x, 'code_x1':val_x1, 'code_x2': val_x2'}]
        """


        out_data = utils.format_data(pmi_sample_data)
        assert out_data == [{'identifier_value': 1, 'date_of_birth': '1900-01-01 00:00:00', 'nhs_number': '000000000'}, {'identifier_value': 2, 'nhs_number': '000000001'}]
        
    def test_filter_data(self):
        """Takes in a list of dictionaries in the following format 
            [{'identifier_value': x, 'code_x1':val_x1, 'code_x2': val_x2'}] 

            And removes any items that don't have BOTH nhs_number and dob
        """
        input_data = [{'identifier_value': 1, 'dob': '19000101', 'nhs_number': '000000000'}, {'identifier_value': 2, 'nhs_number': '000000001'}] 
        out_data = utils.filter_data(input_data)
        
        assert len(out_data) == 1

    def test_format_date_of_birth(self, pmi_sample_data):
        """Converts dob from YYYY-MM-DD 00:00:00 to YYYYMMDD.""" 
        out_data = utils.format_date_of_birth(utils.filter_data(utils.format_data(pmi_sample_data)))

        assert out_data[0]['dob'] == '19000101'


    def test_generate_hash(self, target_data):
        """Checks the hashing algorithm is working as expected."""
        salt = 'dDf2cn9KXp4Js7nw'
        gel_hashes = utils.generate_hash(target_data, salt)
        
        expected_hashes = [x['hash'] for x in target_data]

        assert expected_hashes == gel_hashes

