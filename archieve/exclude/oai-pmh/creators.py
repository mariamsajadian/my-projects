import csv
import pandas as pd
import os
from rdflib import Graph, URIRef
import shutil
import rdflib

result = './result/'
result2 = './creators/'
shutil.rmtree(result2, ignore_errors=True)
os.makedirs(result2, exist_ok=True)

urls = ['mauritshuis',
        'museum-de-fundatie']

# urls = ['mauritshuis',
#         'museum-de-fundatie',
#         'catharijneconvent',
#         'stedelijk-museum-schiedam',
#         'van-abbe-museum',
#         'museum-belvedere',
#         'rijksakademie',
#         'moderne-kunst-museum-deventer']

for url in urls:
    gPath = f'./result/{url}.ttl'
    g = Graph()
    g.parse(gPath, format("ttl"))
    print(url + " Parsed successfully")

    getByIdentifiers = """
    SELECT DISTINCT ?a ?b
    WHERE {
        ?a <http://purl.org/dc/elements/1.1/creator> ?b .
    
    }"""

    qres = g.query(getByIdentifiers)

    with open(result2 + f'creatorForEnrichment_{url}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["uri", "creators"])

        for row in qres:
            sub = row.a.split("/n")[0]
            obj = row.b.split("/n")[0]
            creatorName = "'" + obj + "'"
            writer.writerow([sub, creatorName])

# with open(result2 + f'creatorForEnrichment_{url}.csv', 'r', encoding='utf-8') as fi:
#     fi.read()
#
# data_creators = pd.read_csv(f'./creator-old/creatorForEnrichment_{url}.csv', header=None, names=['URL', 'Creator'])
# removelines = data_creators.replace("\\n", "\n")

# print(removelines)
