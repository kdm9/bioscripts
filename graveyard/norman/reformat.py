import json

# load data json file
data  = json.load(open("HtsSnpsByLocation_detail.json"))

# get records
records = data["response"]["recordset"]["records"]

# make a big dict to hold all the snps
snps = {}

for snp in records:
    snp_id = snp["id"]
    field_lst = snp["fields"]
    fields = {}
    for field in field_lst:
        fields[field["name"]] = field["value"]
    snps[snp_id] = fields

json.dump(snps,open("snps.json", "w"))
