import os
import re
from os.path import basename
import shutil
from rdflib import Graph, URIRef
from sickle import Sickle


def read_files():
    baseUrl = 'https://www.collectienederland.nl/api/oai-pmh/?verb=ListRecords&metadataPrefix=edm-strict&set='

    urls = ['mauritshuis',
            'museum-de-fundatie',
            'catharijneconvent',
            'stedelijk-museum-schiedam',
            'van-abbe-museum',
            'museum-belvedere',
            'rijksakademie',
            'moderne-kunst-museum-deventer']

    shutil.rmtree("./xml_files/", ignore_errors=True)
    os.makedirs("./xml_files/", exist_ok=True)

    for url in urls:
        sickle = Sickle(baseUrl + url)
        records = sickle.ListRecords(metadataPrefix='edm-strict')

        fullPath = "./xml_files/" + url

        i = 0
        for record in records:
            with open(fullPath + '.xml', 'ab+') as fp:
                fp.write(record.raw.encode('utf8'))
            i = i + 1
        print(url + " got records: " + str(i))

        parse_xml(fullPath+'.xml')

    # print(str(i))

    # for fName in os.listdir(path):
    #     if not fName.endswith('.xml'):
    #         continue
    #     fullname = path + "/" + fName
    #     parse_xml(fullname)


def parse_xml(xml_path):
    try:
        content = open(xml_path, 'r', encoding='latin-1').read()
        rdf = re.findall('<rdf:RDF.*?</rdf:RDF>', content, re.DOTALL)
        dir_name = os.path.splitext(basename(xml_path))[0]
        # print(dir_name)

        shutil.rmtree("./files/" + dir_name, ignore_errors=True)
        shutil.rmtree("./result/" + dir_name, ignore_errors=True)
        os.makedirs("./files/" + dir_name, exist_ok=True)
        os.makedirs("./result/" + dir_name, exist_ok=True)
        for idx, p in enumerate(rdf):
            f = open("./files/" + dir_name + "/rdf" + str(idx + 1) + ".xml", "w+", encoding='latin-1')
            if f.write(p):
                f.close()
                process_rdf("./files/" + dir_name + "/rdf" + str(idx + 1) + ".xml", str(idx + 1), dir_name)

    except Exception as e:
        print(str(e))


x = ""


def process_rdf(path, idx, dir_name):
    try:
        global x
        g = Graph()
        g.parse(path, format("xml"), encoding='latin-1')

        # path = "./result/" + dir_name + "/t.ttl"
        path = f'./result/{dir_name}.ttl'
        # g.namespace_manager.bind('schema', URIRef('http://schema.org/'), replace=True)
        xx = g.serialize(format='turtle', encoding='utf8')

        with open(path, "ab+") as myfile:
            myfile.write(xx)
            myfile.close()

    except Exception as e:
        print(str(e))


read_files()

urls = ['mauritshuis',
        'museum-de-fundatie',
        'catharijneconvent',
        'stedelijk-museum-schiedam',
        'van-abbe-museum',
        'museum-belvedere',
        'rijksakademie',
        'moderne-kunst-museum-deventer']

for url in urls:
    gPath = f'./result/{url}.ttl'
    g = Graph()
    g.parse(gPath, format("ttl"))
    print(url + " Parsed successfully")
