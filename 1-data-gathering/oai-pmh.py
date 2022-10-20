import os
import re
from os.path import basename
import shutil
from rdflib import Graph, URIRef
from sickle import Sickle
import argparse

argParser = argparse.ArgumentParser(description="Parse entities")
argParser.add_argument('-e', '--entity', nargs='+', help="Enter entity name")
argParser.add_argument('-u', '--urls', nargs='+', help="Enter API url[s]")
argGroup = argParser.add_mutually_exclusive_group()
argGroup.add_argument('-de', '--default', action='store_true', help="Collect all default entities")
args = argParser.parse_args()

baseUrl = ['https://www.collectienederland.nl/api/oai-pmh/?verb=ListRecords&metadataPrefix=edm-strict&set=']

entities = ['mauritshuis',
            'museum-de-fundatie']

shutil.rmtree("./xml-integrated/", ignore_errors=True)
os.makedirs("./xml-integrated/", exist_ok=True)

shutil.rmtree("./converted/", ignore_errors=True)
os.makedirs("./converted/", exist_ok=True)

def read_files(_baseUrl, _entities):
    for url in _baseUrl:
        for entityName in _entities:
            print(entityName + " proecss started: ")
            sickle = Sickle(url + entityName)
            entityRecords = sickle.ListRecords()
            xmlGather = "./xml-integrated/" + entityName
            i = 0
            for record in entityRecords:
                with open(xmlGather + '.xml', 'ab+') as xmlFile:
                    xmlFile.write(record.raw.encode('utf8'))
                i = i + 1
            print(entityName + " found records: " + str(i))

            parse_xml(xmlGather + '.xml')

def parse_xml(xml_path):
    try:
        rdfContent = open(xml_path, 'r', encoding='utf8').read()
        rdfStriper = re.findall('<rdf:RDF.*?</rdf:RDF>', rdfContent, re.DOTALL)
        entityName = os.path.splitext(basename(xml_path))[0]
        print("Collecting " + entityName)

        shutil.rmtree("./collected/" + entityName, ignore_errors=True)
        os.makedirs("./collected/" + entityName, exist_ok=True)

        for idx, rdfXml in enumerate(rdfStriper):
            f = open("./collected/" + entityName + "/rdf" + str(idx + 1) + ".xml", "w+", encoding='utf8')
            if f.write(rdfXml):
                f.close()
                process_rdf("./collected/" + entityName + "/rdf" + str(idx + 1) + ".xml", entityName)

        ntriples_to_turtle()

    except Exception as e:
        print(str(e))

def process_rdf(rdfXmlPath, dir_name):
    try:
        g = Graph()
        g.parse(rdfXmlPath, format("xml"), encoding='utf-8')
        ntriplesSavePath = f'./converted/{dir_name}.n3'
        ntriples = g.serialize(format='ntriples', encoding='utf-8')

        with open(ntriplesSavePath, "ab+") as saveNtriples:
            saveNtriples.write(ntriples)
            saveNtriples.close()

    except Exception as e:
        print(str(e))

def ntriples_to_turtle(path="./converted"):
    for ntriplesFile in os.listdir(path):
        if not ntriplesFile.endswith('.n3'):
            continue
        entityName = os.path.splitext(basename(ntriplesFile))[0]
        print("this is entityName", entityName)
        ntriplesFilePath = path + "/" + ntriplesFile
        g = Graph()
        g.parse(ntriplesFilePath, format='ntriples')
        g.serialize(destination=f'./converted/{entityName}.ttl', format='turtle', encoding='utf-8')
        print("Converting" + entityName)

if args.entity and args.urls:
    read_files(args.urls, args.entity)
elif not args.entity and args.urls:
    read_files(args.urls, entities)
elif args.entity and not args.urls:
    read_files(baseUrl, args.entity)
elif __name__ == '__main__' or args.default:
    read_files(baseUrl, entities)
