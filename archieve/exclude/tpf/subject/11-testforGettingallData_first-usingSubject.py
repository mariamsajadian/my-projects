import os
import re
import shutil
import rdflib
import requests
from os.path import basename

url_id = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://purl.org/dc/elements/1.1/identifier'
url_agg = 'https://data.collectienederland.nl/fragments/mauritshuis?predicate=http://www.europeana.eu/schemas/edm/provider'
folders = url_id.split("?")[0].split("/")[-1]
result = f'./testfileforsubject/{folders}/'
shutil.rmtree(result, ignore_errors=True)
os.makedirs(result, exist_ok=True)

def collectURLs(result, url,name):
    response = requests.get(url)
    with open(result  + f'subjects_{name}.ttl', 'w', encoding='utf-8') as f:
        f.write(response.text)
    g2 = rdflib.Graph()
    g2.parse(result + f'subjects_{name}.ttl', format='ttl', encoding='utf-8')
    getByIdentifiers = """
    SELECT DISTINCT ?a
    WHERE {
        ?a ?p ?b .
    
    }"""

    qres = g2.query(getByIdentifiers)
    try:
        with open(result + f'subjects_{name}_urls.txt', 'w', encoding='utf-8') as f:
            for row in qres:
                allsubject_Doc = row.a
                if 59 < len(allsubject_Doc) < 75:
                    url_Doc = f'https://data.collectienederland.nl/fragments/mauritshuis?subject={allsubject_Doc}\n'
                    f.write(url_Doc)
    except Exception as e:
        print("There is an Error in request:", str(e))

collectURLs(result, url_id,name="doc")
collectURLs(result, url_agg,name="agg")

def margeURLfiles(path=result):
    listname = []
    for fName in os.listdir(path):
        if not fName.endswith('_urls.txt'):
            continue
        fullname = path + fName
        listname.append(fullname)
    with open(path + 'URLS_final.txt', 'w', encoding='utf-8') as outfile:
        for names in listname:
            print(names)
            with open(names) as eachfile:
                outfile.write(eachfile.read())
            outfile.write("\n")
            print("urls are marged")

margeURLfiles(path=result)

with open(result + 'URLS_final.txt', 'r', encoding='utf-8') as data:
    for idx, url in enumerate(data):
        print(url)
        if not url.strip():
            continue
        print("this is my data please click on url and see data in google chrome:", url)

        response = requests.get(url)
        print(response.status_code)
        with open(result + f'allData{idx}.ttl', 'w', encoding='utf-8') as f:
            f.write(response.text)

            print("there is not data provider and right in the fragments URLs and also for document urls I donot have tiltle and creator and other datasets ")