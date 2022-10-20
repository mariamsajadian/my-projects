import csv
import os
import shutil

from rdflib import Graph, BNode
from rdflib.namespace import Namespace

resultArtForm = './art-form/'
shutil.rmtree(resultArtForm, ignore_errors=True)
os.makedirs(resultArtForm, exist_ok=True)

resultCreatorsCsv = './creators/'
shutil.rmtree(resultCreatorsCsv, ignore_errors=True)
os.makedirs(resultCreatorsCsv, exist_ok=True)


edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")


# def read_files(path="./converted/"):
#     for fName in os.listdir(path):
#         if not fName.endswith('.ttl'):
#             continue
#         dataStore = path + "/" + fName
        # parse_xml(fullname)
        # print("RDFXML files converted to turtle: see result folder")

dataStore = "./converted/"
entities = [
    'mauritshuis',
    # 'museum-de-fundatie',
    # 'museum-belvedere',
    # 'moderne-kunst-museum-deventer'
]

# urls = ['mauritshuis',
#         'museum-de-fundatie',
#         'catharijneconvent',
#         'stedelijk-museum-schiedam',
#         'van-abbe-museum',
#         'museum-belvedere',
#         'rijksakademie',
#         'moderne-kunst-museum-deventer']


def extractArtform(dataStore, entities, aat, dcterms, rdf, edm, resultArtForm):
    for entityName in entities:
        gPath = f'{dataStore}{entityName}.ttl'
        g = Graph()
        g.parse(gPath, format("ttl"))
        print(entityName + " parsed successfully")
        getByIdentifiers = """  
        SELECT DISTINCT ?s ?p ?o 
        WHERE {
            ?s ?p ?o .  
        }"""
        queryResult = g.query(getByIdentifiers)
        for index, row in enumerate(queryResult):
            if str(row.p) == 'http://www.europeana.eu/schemas/edm/type':
                g.add((row.s, edm['image'], BNode(index)))
                g.add((BNode(index), rdf['type'], edm['ImageObject']))
            if str(row.p) == 'http://purl.org/dc/elements/1.1/type':
                if str(row.o) == 'schilderij':
                    g.add((row.s, dcterms.Type, aat['300020756']))
                if str(row.o) == 'painting':
                    g.add((row.s, dcterms.Type, aat['300020756']))
                if str(row.o) == 'miniatuur':
                    g.add((row.s, dcterms.Type, aat['300033936']))
                if str(row.o) == 'miniature':
                    g.add((row.s, dcterms.Type, aat['300033936']))
                if str(row.o) == 'pastel':
                    g.add((row.s, dcterms.Type, aat['300076922']))
                if str(row.o) == 'aquarel':
                    g.add((row.s, dcterms.Type, aat['300404216']))
                if str(row.o) == 'olieverfschilderij':
                    g.add((row.s, dcterms.Type, aat['300404216']))
                if str(row.o) == 'watercolor':
                    g.add((row.s, dcterms.Type, aat['300078925']))
        g.serialize(destination=f'{resultArtForm}{entityName}.ttl', format='turtle', encoding='utf-8')
        print("art form created! successfully")


def extractCsvCreators(entities, resultArtForm, resultCreatorsCsv):
    for entityName in entities:
        gPath = f'{resultArtForm}{entityName}.ttl'
        g = Graph()
        g.parse(gPath, format("ttl"))
        print(entityName + " Parsed successfully")

        getByIdentifiers = """
        SELECT DISTINCT ?a ?b ?c
        WHERE {
            ?a <http://purl.org/dc/elements/1.1/creator> ?b .
            ?a <http://purl.org/dc/terms/Type> ?c.    
        }"""

        queryResult = g.query(getByIdentifiers)
        with open(resultCreatorsCsv + f'creatorWithType_{entityName}.csv', 'w', encoding='utf-8',
                  newline='') as fileHanler:
            writer = csv.writer(fileHanler, delimiter=',')
            writer.writerow(["uri", "creators", "type"])
            for row in queryResult:
                sub = row.a.split("/n")[0]
                obj = row.b.split("/n")[0]
                creatorName = "'" + obj.replace('"', "") + "'"
                obj2 = row.c.split("/n")[0]
                writer.writerow([sub, creatorName, obj2])

        with open(resultCreatorsCsv + f'creatorWithoutType_{entityName}.csv', 'w', encoding='utf-8',
                  newline='') as fileHanler:
            writer = csv.writer(fileHanler, delimiter=',')
            writer.writerow(["uri", "creators"])
            for row in queryResult:
                sub = row.a.split("/n")[0]
                obj = row.b.split("/n")[0]
                creatorName = obj.replace('"', '')
                if '"' not in creatorName:
                    creatorName = "'" + creatorName + "'"
                writer.writerow([sub, str(creatorName)])


extractArtform(dataStore, entities, aat, dcterms, rdf, edm, resultArtForm)
extractCsvCreators(entities, resultArtForm, resultCreatorsCsv)
