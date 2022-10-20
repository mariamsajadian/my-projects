from rdflib import Graph, URIRef, Literal, BNode
import os
import shutil


filename = 'mauritshuis.ttl'
path = f'./EnrichStepOne/{filename}'
result = f'./EnrichSparql/'
shutil.rmtree(result, ignore_errors=True)
os.makedirs(result, exist_ok=True)
g_data = Graph().parse(path)
print("done0!")
with open('EnrichQ1.rq') as file:
    query_txt = file.read()
    res = g_data.query(query_txt)
print("done1!")
res.serialize(f'{result}m_result.n3', format='ntriples') #N3 fine
g = Graph()
g.parse(f'{result}m_result.n3', format='ntriples')
g.namespace_manager.bind('schema', URIRef('http://schema.org/'), replace=True)
g.serialize(destination=f'{result}m_final.ttl', format='turtle', encoding='utf-8')
print("done2!")