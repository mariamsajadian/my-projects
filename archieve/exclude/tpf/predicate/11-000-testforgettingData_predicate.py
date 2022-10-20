import csv
import os
import re
import shutil
import rdflib
import requests
from os.path import basename

url_id = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://purl.org/dc/elements/1.1/identifier'
url_type = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://purl.org/dc/elements/1.1/type'
url_title = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://purl.org/dc/elements/1.1/title'
url_creator = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://purl.org/dc/elements/1.1/creator'
url_created = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://purl.org/dc/terms/created'
url_extend = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://purl.org/dc/terms/extent'
url_date = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://purl.org/dc/elements/1.1/date'
url_provider = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://www.europeana.eu/schemas/edm/provider'
url_dataProvider = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://www.europeana.eu/schemas/edm/dataProvide'
url_right = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://www.europeana.eu/schemas/edm/rights'


# folders = url_id.split("?")[0].split("/")[-1]
result ='./testfile/'
shutil.rmtree(result, ignore_errors=True)
os.makedirs(result, exist_ok=True)


def collectURLs(result, url, name):

    response = requests.get(url)
    with open(result + f'predicate_{name}.ttl', 'w', encoding='utf-8') as f:
        f.write(response.text)
    # g2 = rdflib.Graph()
    # g2.parse(result + f'predicate_{name}.ttl', format='ttl', encoding='utf-8')
    # getByIdentifiers = """
    # SELECT DISTINCT ?a
    # WHERE {
    #     ?a ?p ?b .
    #
    # }"""
    #
    # qres = g2.query(getByIdentifiers)
    # try:
    #     with open(result + f'predicate_{name}_urls.txt', 'w', encoding='utf-8') as f:
    #         for row in qres:
    #             print(row.a, row.b)
    # except Exception as e:
    #     print("There is an Error in request:", str(e))


collectURLs(result, url_id, name="doc")
collectURLs(result, url_type, name="type")
collectURLs(result, url_title, name="title")
collectURLs(result,url_creator,name='creator')
collectURLs(result,url_created,name='created')
collectURLs(result,url_extend,name='extend')
collectURLs(result,url_date,name='date')
collectURLs(result,url_provider,name='provider')
collectURLs(result,url_dataProvider,name='dataProvider')
collectURLs(result,url_right,name='right')

g2 = rdflib.Graph()
g2.parse(result + f'predicate_creator.ttl', format='ttl', encoding='utf-8')
getByIdentifiers = """
SELECT DISTINCT ?a ?b
WHERE {
    ?a <http://purl.org/dc/elements/1.1/creator> ?b .

}"""

qres = g2.query(getByIdentifiers)

with open(result + f'creatorForEnrichment.csv', 'w', encoding='utf-8') as f:
        for row in qres:
            sub = row.a.split("/n")
            obj = row.b.split("/n")
            writer = csv.writer(f, delimiter=',')
            writer.writerows(zip(sub, obj))



