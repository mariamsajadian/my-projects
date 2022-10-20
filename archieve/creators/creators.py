import csv
import pandas as pd
import os
from rdflib import Graph, URIRef
import shutil
import rdflib

# result = './Enrich1/'
result2 = './creators/'
shutil.rmtree(result2, ignore_errors=True)
os.makedirs(result2, exist_ok=True)

url = 'mauritshuis'


# urls = ['mauritshuis',
#         'museum-de-fundatie',
#         'catharijneconvent',
#         'stedelijk-museum-schiedam',
#         'van-abbe-museum',
#         'museum-belvedere',
#         'rijksakademie',
#         'moderne-kunst-museum-deventer']

# for url in urls:
gPath = f'./Enrich1/{url}.ttl'
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

with open(result2 + f'creatorForEnrichment_{url}.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(["uri", "creators", "type"])

    for row in qres:
        print(row.c)
        sub = row.a.split("/n")[0]
        obj = row.b.split("/n")[0]
        creatorName = "'" + obj + "'"
        obj2 = row.c.split("/n")[0]
        writer.writerow([sub, creatorName, obj2])

