import csv
import pandas as pd
import os
from rdflib import Graph, URIRef
import shutil
import rdflib

# result = './Enrich1/'
result_creators_csv = './creators/'
shutil.rmtree(result_creators_csv, ignore_errors=True)
os.makedirs(result_creators_csv, exist_ok=True)

# url = 'mauritshuis'
# url= 'moderne-kunst-museum-deventer'


urls = ['mauritshuis',
        'museum-de-fundatie',
        'museum-belvedere',
        'moderne-kunst-museum-deventer']


for url in urls:
    gPath = f'./EnrichStepOne/{url}.ttl'
    g = Graph()
    g.parse(gPath, format("ttl"))
    print(url + " Parsed successfully")

    getByIdentifiers = """
    SELECT DISTINCT ?a ?b ?c
    WHERE {
        ?a <http://purl.org/dc/elements/1.1/creator> ?b .
        ?a <http://purl.org/dc/terms/Type> ?c.
    
    }"""

    qres = g.query(getByIdentifiers)

    with open(result_creators_csv + f'creatorWithType_{url}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["uri", "creators", "type"])

        for row in qres:
            sub = row.a.split("/n")[0]
            obj = row.b.split("/n")[0]
            creatorName = "'" + obj.replace('"', "") + "'"
            obj2 = row.c.split("/n")[0]
            writer.writerow([sub, creatorName, obj2])

    with open(result_creators_csv + f'creatorWithoutType_{url}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["uri", "creators"])

        for row in qres:
            sub = row.a.split("/n")[0]
            obj = row.b.split("/n")[0]
            obj = obj.replace('"', "")
            creatorName = "'" + obj.replace('"', "") + "'"
            writer.writerow([sub, creatorName])