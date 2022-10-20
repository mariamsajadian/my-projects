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

schema = Namespace("http://www.schema.org/type")
edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

dataStore = "./converted/"
entities = [
        'mauritshuis',
            'museum-de-fundatie',
            'museum-belvedere',
            'moderne-kunst-museum-deventer'
            ]

# urls = ['mauritshuis',
#         'museum-de-fundatie',
#         'catharijneconvent',
#         'stedelijk-museum-schiedam',
#         'van-abbe-museum',
#         'museum-belvedere',
#         'rijksakademie',
#         'moderne-kunst-museum-deventer']


def extract_artform(_dataStore, _entities, _aat, _dcterms, _rdf, _edm, _resultArtForm):
    for entityName in _entities:
        gPath = f'{_dataStore}{entityName}.ttl'
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
                g.add((row.s, _edm['image'], BNode(index)))
                g.add((BNode(index), _rdf['type'], _edm['ImageObject']))
            if str(row.p) == 'http://purl.org/dc/elements/1.1/type':
                if str(row.o) == 'schilderij':
                    g.add((row.s, _dcterms.Type, _aat['300020756']))
                if str(row.o) == 'painting':
                    g.add((row.s, _dcterms.Type, _aat['300020756']))
                if str(row.o) == 'miniatuur':
                    g.add((row.s, _dcterms.Type, _aat['300033936']))
                if str(row.o) == 'miniature':
                    g.add((row.s, _dcterms.Type, _aat['300033936']))
                if str(row.o) == 'pastel':
                    g.add((row.s, _dcterms.Type, _aat['300076922']))
                if str(row.o) == 'aquarel':
                    g.add((row.s, _dcterms.Type, _aat['300404216']))
                if str(row.o) == 'olieverfschilderij':
                    g.add((row.s, _dcterms.Type, _aat['300404216']))
                if str(row.o) == 'watercolor':
                    g.add((row.s, _dcterms.Type, _aat['300078925']))
        g.serialize(destination=f'{_resultArtForm}{entityName}.ttl', format='turtle', encoding='utf-8')
        print("art form created! successfully")


def extract_csv_creators(_entities, _resultArtForm, _resultCreatorsCsv):
    for entityName in _entities:
        gPath = f'{_resultArtForm}{entityName}.ttl'
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
        with open(_resultCreatorsCsv + f'creatorWithType_{entityName}.csv', 'w', encoding='utf-8', newline='') as fileHanler:
            writer = csv.writer(fileHanler, delimiter=',')
            writer.writerow(["uri", "creators", "type"])
            for row in queryResult:
                sub = row.a.split("/n")[0]
                obj = row.b.split("/n")[0]
                creatorName = "'" + obj.replace('"', "") + "'"
                obj2 = row.c.split("/n")[0]
                writer.writerow([sub, creatorName, obj2])

        with open(_resultCreatorsCsv + f'creatorWithoutType_{entityName}.csv', 'w', encoding='utf-8', newline='') as fileHanler:
            writer = csv.writer(fileHanler, delimiter=',')
            writer.writerow(["uri", "creators"])
            for row in queryResult:
                sub = row.a.split("/n")[0]
                obj = row.b.split("/n")[0]
                creatorName1 = obj.replace('"', '')
                creatorName = creatorName1.strip(' " " ')
                writer.writerow([sub, creatorName])


extract_artform(dataStore, entities, aat, dcterms, rdf, edm, resultArtForm)
extract_csv_creators(entities, resultArtForm, resultCreatorsCsv)
