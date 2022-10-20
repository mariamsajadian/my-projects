import csv
import rdflib
import re
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import FOAF, NamespaceManager, Namespace, RDFS
import os
import shutil


result = './EnrichStepOne/'
shutil.rmtree(result, ignore_errors=True)
os.makedirs(result, exist_ok=True)
schema = Namespace("http://www.schema.org/type")
edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")


urls = ['mauritshuis',
        'museum-de-fundatie',
        'museum-belvedere',
        'moderne-kunst-museum-deventer']


for url in urls:
    gPath = f'./result/ok/{url}.ttl'
    g = Graph()
    g.parse(gPath, format("ttl"))
    print(url + " Parsed successfully")
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
            elif dateOfCreation_forComparison >= 1750 and dateOfCreation_forComparison < 1850:
                g.add((row.s, edm.temporalCoverage, aat['300172863000']))
                g.add((aat['300172863000'], dcterms.startDate, Literal("1750", datatype=XSD.string)))
                g.add((aat['300172863000'], dcterms.endDate, Literal("1850", datatype=XSD.string)))
                g.add((aat['300172863000'], dcterms.name, Literal("Classicism ", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1780 and dateOfCreation_forComparison < 1850:
                g.add((row.s, edm.temporalCoverage, aat['300172863']))
                g.add((aat['300172863'], dcterms.startDate, Literal("1780", datatype=XSD.string)))
                g.add((aat['300172863'], dcterms.endDate, Literal("1850", datatype=XSD.string)))
                g.add((aat['300172863'], dcterms.name, Literal("Romantic", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1830 and dateOfCreation_forComparison < 1870:
                g.add((row.s, edm.temporalCoverage, aat['300172861']))
                g.add((aat['300172861'], dcterms.startDate, Literal("1830", datatype=XSD.string)))
                g.add((aat['300172861'], dcterms.endDate, Literal("1870", datatype=XSD.string)))
                g.add((aat['300172861'], dcterms.name, Literal("Realist", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1860 and dateOfCreation_forComparison < 1890:
                g.add((row.s, edm.temporalCoverage, aat['300021503']))
                g.add((aat['300021503'], dcterms.startDate, Literal("1860", datatype=XSD.string)))
                g.add((aat['300021503'], dcterms.endDate, Literal("1890", datatype=XSD.string)))
                g.add((aat['300021503'], dcterms.name, Literal("Impressionist", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1890 and dateOfCreation_forComparison < 1970:
                g.add((row.s, edm.temporalCoverage, aat['300021474']))
                g.add((aat['300021474'], dcterms.startDate, Literal("1890", datatype=XSD.string)))
                g.add((aat['300021474'], dcterms.endDate, Literal("1970", datatype=XSD.string)))
                g.add((aat['300021474'], dcterms.name, Literal("Modernist", datatype=XSD.string)))
                continue
            elif dateOfCreation_forComparison >= 1970:
                g.add((row.s, edm.temporalCoverage, aat['300022208']))
                g.add((aat['300022208'], dcterms.startDate, Literal("1970", datatype=XSD.string)))
                g.add((aat['300022208'], dcterms.endDate, Literal("Now", datatype=XSD.string)))
                g.add((aat['300022208'], dcterms.name, Literal("Postmodern", datatype=XSD.string)))
                continue
    g.serialize(destination=f'{result}{url}.ttl', format='turtle', encoding='utf-8')

    print(" Done! successfully")