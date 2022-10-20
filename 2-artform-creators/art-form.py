import csv
import os
import shutil
import traceback
from rdflib import Graph, BNode
from rdflib.namespace import Namespace

schema = Namespace("http://www.schema.org/type")
edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")


def startProcessing(_path="./converted/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
        extract_artform(_path, _entities, aat, dcterms, rdf, edm)
        extract_csv_creators(_entities)
    except Exception as e:
        print(str(e), traceback.format_exc())


def extract_artform(_dataStore, _entities, _aat, _dcterms, _rdf, _edm, _resultArtForm='./art-form/'):

    shutil.rmtree(_resultArtForm, ignore_errors=True)
    os.makedirs(_resultArtForm, exist_ok=True)

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


def extract_csv_creators(_entities, _resultArtForm='./art-form/', _resultCreatorsCsv='./creators/'):

    shutil.rmtree(_resultCreatorsCsv, ignore_errors=True)
    os.makedirs(_resultCreatorsCsv, exist_ok=True)

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
        with open(_resultCreatorsCsv + f'creatorWithType_{entityName}.csv', 'w', encoding='utf-8',
                  newline='') as fileHanler:
            writer = csv.writer(fileHanler, delimiter=',')
            writer.writerow(["uri", "creators", "type"])
            for row in queryResult:
                sub = row.a.split("/n")[0]
                obj = row.b.split("/n")[0]
                creatorName = "'" + obj.replace('"', "") + "'"
                obj2 = row.c.split("/n")[0]
                writer.writerow([sub, creatorName, obj2])

        with open(_resultCreatorsCsv + f'creatorWithoutType_{entityName}.csv', 'w', encoding='utf-8',
                  newline='') as fileHanler:
            writer = csv.writer(fileHanler, delimiter=',', quotechar="\'", quoting=csv.QUOTE_NONE, escapechar=' ')
            writer.writerow(["uri", "creators"])
            for row in queryResult:
                sub = row.a.split("/n")[0]
                obj = str(row.b.split("/n")[0])
                creatorNameStripped = obj.__str__().replace('"', '')
                creatorName = '"{}"'.format(creatorNameStripped)
                writer.writerow([sub, creatorName])

startProcessing()
