import json
import os

state_data = {}
district_data = {}
all_districts = {}
ward_data = {}
all_wards = {}
DISTRICT_LOOKUP_CHANNEL = 'districts'
WARD_LOOKUP_CHANNEL = 'wards'

data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'json_data')

with open(data_path + '/tinh_tp.json', 'r', encoding='utf-8') as fp:
    state_data.update(json.load(fp))

with open(data_path + '/quan_huyen.json', 'r', encoding='utf-8') as fp:
    district_data.update(json.load(fp))

with open(data_path + '/xa_phuong.json', 'r', encoding='utf-8') as fp:
    ward_data.update(json.load(fp))

with open(data_path + '/quan_huyen_all.json', 'r', encoding='utf-8') as fp:
    all_districts.update(json.load(fp))
