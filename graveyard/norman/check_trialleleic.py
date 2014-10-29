import json

snps = json.load(open("snps.json"))

for snp_id, fields in snps.iteritems():
    if len(fields["comp_alleles"]) > 1:
        print "%s is multi-allelic (%s)" %  (snp_id, fields["comp_alleles"])
