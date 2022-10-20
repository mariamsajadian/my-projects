import csv
import rdflib
import re
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import FOAF, NamespaceManager, Namespace, RDFS
import os
import shutil

result = './result/'
result2 = './Enrich5filestest/'
shutil.rmtree(result2, ignore_errors=True)
os.makedirs(result2, exist_ok=True)
schema = Namespace("http://www.schema.org/type")
edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
# urls = ['mauritshuis',
#         'catharijneconvent',
#         'stedelijk-museum-schiedam',
#         'van-abbe-museum',
#         'museum-belvedere' ]
urls = ['mauritshuis',
        'catharijneconvent' ]

for url in urls:
    gPath = f'./result/{url}.ttl'
    g = Graph()
    g.parse(gPath, format("ttl"))
    print(url + " Parsed successfully")
    getByIdentifiers = """  
    SELECT DISTINCT ?s ?p ?o 
    WHERE {
        ?s ?p ?o .
        OPTIONAL{ 
    ?s dc:type ?o 
FILTER( ?o != "pastel" ) }
    }"""
    qres = g.query(getByIdentifiers)
    for index, row in enumerate(qres):
        if (str(row.p) == 'http://www.europeana.eu/schemas/edm/type'):
            g.add((row.s, edm['image'], BNode(index)))
            g.add((BNode(index), rdf['type'], edm['ImageObject']))
        if (str(row.p) == "http://purl.org/dc/terms/created"):
            dateOfCreation = str(row.o)
            match = re.search(r'\d{4}', dateOfCreation)
            if match and match.group(0) is not None:
                dateOfCreation_forComparison = int(match.group(0))
                Date = str(match.group(0))
            else:
                continue
            g.add((row.s, dcterms.dateCreated, Literal(Date)))
            g.add((row.s, dcterms.temporal, Literal(dateOfCreation)))
            if dateOfCreation_forComparison >= 1000 and dateOfCreation_forComparison < 1450:
                g.add((row.s, edm.temporalCoverage, aat['300020756']))
                g.add((aat['300020756'], dcterms.startDate, Literal("1000", datatype=XSD.string)))
                g.add((aat['300020756'], dcterms.endDate, Literal("1450", datatype=XSD.string)))
                g.add((aat['300020756'], dcterms.name, Literal("Medieval", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1450 and dateOfCreation_forComparison < 1600:
                g.add((row.s, edm.temporalCoverage, aat['300021140']))
                g.add((aat['300021140'], dcterms.startDate, Literal("1450", datatype=XSD.string)))
                g.add((aat['300021140'], dcterms.endDate, Literal("1600", datatype=XSD.string)))
                g.add((aat['300021140'], dcterms.name, Literal("Renaissance", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1600 and dateOfCreation_forComparison < 1750:
                g.add((row.s, edm.temporalCoverage,  aat['300021147']))
                g.add((aat['300021147'], dcterms.startDate, Literal("1600", datatype=XSD.string)))
                g.add((aat['300021147'], dcterms.endDate, Literal("1750", datatype=XSD.string)))
                g.add((aat['300021147'], dcterms.name, Literal("Baroque", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1750 and dateOfCreation_forComparison < 1830:
                g.add((row.s, edm.temporalCoverage, aat['300172863']))
                g.add((aat['300172863'], dcterms.startDate, Literal("1750", datatype=XSD.string)))
                g.add((aat['300172863'], dcterms.endDate, Literal("1830", datatype=XSD.string)))
                g.add((aat['300172863'], dcterms.name, Literal("Romantic", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1830 and dateOfCreation_forComparison < 1870:
                g.add((row.s, edm.temporalCoverage, aat['300172861']))
                g.add((aat['300172861'], dcterms.startDate, Literal("1830", datatype=XSD.string)))
                g.add((aat['300172861'], dcterms.endDate, Literal("1870", datatype=XSD.string)))
                g.add((aat['300172861'], dcterms.name, Literal("Realist", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1870 and dateOfCreation_forComparison < 1890:
                g.add((row.s, edm.temporalCoverage, aat['300021503']))
                g.add((aat['300021503'], dcterms.startDate, Literal("1870", datatype=XSD.string)))
                g.add((aat['300021503'], dcterms.endDate, Literal("1890", datatype=XSD.string)))
                g.add((aat['300021503'], dcterms.name, Literal("Impressionist", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1870:
                g.add((row.s, edm.temporalCoverage, aat['300022208']))
                g.add((aat['300022208'], dcterms.startDate, Literal("1870", datatype=XSD.string)))
                g.add((aat['300022208'], dcterms.endDate, Literal("Now", datatype=XSD.string)))
                g.add((aat['300022208'], dcterms.name, Literal("Postmodern", datatype=XSD.string)))
                continue
    g.serialize(destination=f'{result2}{url}.ttl', format='turtle', encoding='utf-8')

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
grdf.parse(f'{result2}mauritshuis.ttl', format='turtle')

mauritshuis_Graph = gCSV + grdf

print(type(mauritshuis_Graph))

mauritshuis_Graph.serialize(destination=f'mauritshuis_Graph.ttl', format='turtle', encoding='utf-8')

print(" Done! successfully")