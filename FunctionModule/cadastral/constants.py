import json
import os

state_data = {}
district_data = {}
ward_data = {}
DISTRICT_LOOKUP_CHANNEL = 'districts'
WARD_LOOKUP_CHANNEL = 'wards'


dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + '/tinh_tp.json') as fp:
    state_data.update(json.load(fp))

with open(dir_path + '/quan_huyen.json') as fp:
    district_data.update(json.load(fp))

with open(dir_path + '/xa_phuong.json') as fp:
    ward_data.update(json.load(fp))
