import json
from os import listdir
from os.path import isfile, join

mypath = 'xa-phuong'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
xa_phuong = {}

for f in onlyfiles:
    with open(f"{mypath}/{f}") as fp:
        code = f[0:-5]
        try:
            data = json.load(fp, encoding='utf-8')
            xa_phuong[code] = [v for k,v in data.items()]
        except:
            pass

with open('test.json', 'w', encoding='utf-8') as fp:
    json.dump(xa_phuong, fp, ensure_ascii=False)

# with open('tinh_tp.json') as fp:
#     data = json.load(fp, encoding='utf-8')
#     sorted_keys = sorted(data)
#     new = {}
#     for item in sorted_keys:
#         new[item] = data[item]
# with open('tinh_tp.json', 'w', encoding='utf-8') as fp:
#     json.dump(new, fp, ensure_ascii=False)
