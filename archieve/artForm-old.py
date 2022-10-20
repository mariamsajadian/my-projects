from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import FOAF, NamespaceManager, Namespace, RDFS
import os
import shutil
import csv

result_artForm = './art-form/'
shutil.rmtree(result_artForm, ignore_errors=True)
os.makedirs(result_artForm, exist_ok=True)

result_creators_csv = './creators/'
shutil.rmtree(result_creators_csv, ignore_errors=True)
os.makedirs(result_creators_csv, exist_ok=True)

schema = Namespace("http://www.schema.org/type")
edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

datasource = "./converted/"
_entities = ['mauritshuis',
        'museum-de-fundatie',
        'museum-belvedere',
        'moderne-kunst-museum-deventer']

# urls = ['mauritshuis',
#         'museum-de-fundatie',
#         'catharijneconvent',
#         'stedelijk-museum-schiedam',
#         'van-abbe-museum',
#         'museum-belvedere',
#         'rijksakademie',
#         'moderne-kunst-museum-deventer']

def extract_artform( _entities,aat,dcterms, rdf, edm, result_artForm):
    for entityName in _entities:
        gPath = f'{datasource}{entityName}.ttl'
        g = Graph()
        g.parse(gPath, format("ttl"))
        print(entityName + " Parsed successfully")
        getByIdentifiers = """  
        SELECT DISTINCT ?s ?p ?o 
        WHERE {
            ?s ?p ?o .  
        }"""
        qres = g.query(getByIdentifiers)
        for index, row in enumerate(qres):
            if (str(row.p) == 'http://www.europeana.eu/schemas/edm/type'):
                g.add((row.s, edm['image'], BNode(index)))
                g.add((BNode(index), rdf['type'], edm['ImageObject']))
            if (str(row.p) == 'http://purl.org/dc/elements/1.1/type' ):
                if(str(row.o) == 'schilderij'):
                    g.add((row.s, dcterms.Type, aat['300020756']))
                if(str(row.o) == 'painting'):
                    g.add((row.s, dcterms.Type, aat['300020756']))
                if(str(row.o) == 'miniatuur' ):
                    g.add((row.s, dcterms.Type, aat['300033936']))
                if(str(row.o) == 'miniature' ):
                    g.add((row.s, dcterms.Type, aat['300033936']))
                if(str(row.o) == 'pastel' ):
                    g.add((row.s, dcterms.Type, aat['300076922']))
                if(str(row.o) == 'aquarel' ):
                    g.add((row.s, dcterms.Type, aat['300404216']))
                if(str(row.o) == 'olieverfschilderij' ):
                    g.add((row.s, dcterms.Type, aat['300404216']))
                if(str(row.o) == 'watercolor' ):
                    g.add((row.s, dcterms.Type, aat['300078925']))
        g.serialize(destination=f'{result_artForm}{entityName}.ttl', format='turtle', encoding='utf-8')
        print("art form created! successfully")

def extract_csv_creators( _entities, result_artForm, result_creators_csv):
    for entityName in _entities:
        gPath = f'{result_artForm}{entityName}.ttl'
        g = Graph()
        g.parse(gPath, format("ttl"))
        print(entityName + " Parsed successfully")

        getByIdentifiers = """
        SELECT DISTINCT ?a ?b ?c
        WHERE {
            ?a <http://purl.org/dc/elements/1.1/creator> ?b .
            ?a <http://purl.org/dc/terms/Type> ?c.    
        }"""

        qres = g.query(getByIdentifiers)
        with open(result_creators_csv + f'creatorWithType_{entityName}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["uri", "creators", "type"])
            for row in qres:
                sub = row.a.split("/n")[0]
                obj = row.b.split("/n")[0]
                creatorName = "'" + obj.replace('"', "") + "'"
                obj2 = row.c.split("/n")[0]
                writer.writerow([sub, creatorName, obj2])

        with open(result_creators_csv + f'creatorWithoutType_{entityName}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["uri", "creators"])
            for row in qres:
                sub = row.a.split("/n")[0]
                obj = row.b.split("/n")[0]
                obj = obj.replace('"', "")
                creatorName = "'" + obj.replace('"', "") + "'"
                writer.writerow([sub, creatorName])

extract_artform( _entities,aat,dcterms, rdf, edm, result_artForm)
extract_csv_creators( _entities, result_artForm, result_creators_csv)