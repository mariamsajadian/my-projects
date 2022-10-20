
import csv
import rdflib
import re
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import FOAF, NamespaceManager, Namespace, RDFS
import os
import shutil
schema = Namespace("http://www.schema.org/type")
edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

result_integration = './enrich-integration/'
shutil.rmtree(result_integration, ignore_errors=True)
os.makedirs(result_integration, exist_ok=True)

g = Graph()
filename = 'creatorForEnrichment_mauritshuis.csv'
i = 0
with open(filename) as csvfile:
    datareader = csv.reader(csvfile, delimiter=';')

    for row in datareader:
        if i == 0:
            i = 1
            continue
        g.add((URIRef(row[0]), dc.creator, URIRef(row[2])))
        g.add((URIRef(row[2]), rdf.type, dc.Person))
        g.add((URIRef(row[2]), dc.name,  Literal(row[1])))
        g.namespace_manager.bind('dc', URIRef('http://purl.org/dc/elements/1.1'), replace=True)
        g.namespace_manager.bind('rdf', URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'), replace=True)

g.serialize(destination=f'creators_test.ttl', format='turtle', encoding='utf-8')

gRemove = rdflib.Graph()
gRemove.parse('creators_test.ttl', format("ttl"))

removecharacters = """
  SELECT DISTINCT ?b
  WHERE {
      ?s ?p ?o .
      filter(?s != <>)
      filter(?s != <file:///C:/Taxonic/00Project/0-startPoint/pythoncodes/0-rdfxmlToRDF/1-xmlprocessing/NewOAI_API/ttl> )
  }"""
gRemove.query(removecharacters)
gRemove.serialize(destination=f'creators_test2.ttl', format='turtle', encoding='utf-8')

gCSV = Graph()
gCSV.parse(f'creators_test2.ttl', format='turtle')

grdf = Graph()
grdf.parse(f'{result_integration}mauritshuis.ttl', format='turtle')

mauritshuis_Graph = gCSV + grdf

print(type(mauritshuis_Graph))

mauritshuis_Graph.serialize(destination=f'mauritshuis_Graph.ttl', format='turtle', encoding='utf-8')

print(" Done! successfully")