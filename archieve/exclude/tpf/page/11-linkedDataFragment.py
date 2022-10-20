import os
import shutil
import requests
import rdflib

url = 'https://data.collectienederland.nl/fragments/mauritshuis'
gPage = rdflib.Graph()
gPage.parse(url)
pageLimit = """
  SELECT DISTINCT ?b
  WHERE {
      ?a <http://www.w3.org/ns/hydra/core#itemsPerPage> ?b .

  }"""
qresforpage = gPage.query(pageLimit)

for row in qresforpage:
  print("this is page number:", (int(row.b)))
result = "./result_API_raw/"

shutil.rmtree(result, ignore_errors=True)
os.makedirs(result, exist_ok=True)
# pageLimit = int(row.b)
pageLimit = 3
response = requests.get(url)
all_triples_text = ''
pageCount = 1
g_all = rdflib.Graph()

try:
  while pageCount < pageLimit:
    current_page_url = url + '?page=' + str(pageCount)
    print(f'Currently fetching page {current_page_url}')
    response = requests.get(current_page_url)
    if response.status_code != 200:
      print('---------------------------------------')
      print(f'last page: please check the last output page, if it is empty delete it')
      print('---------------------------------------')
      break

    with open(result + f'page_{pageCount}.ttl', 'w', encoding='utf-8') as f:
      f.write(response.text)
    g2 = rdflib.Graph()
    g_all += g2.parse(result + f'page_{pageCount}.ttl', format='ttl', encoding='utf-8')
    pageCount += 1
    # print(len(g_all))
except Exception as e:
  print("There is not more pages. please check that last page in your folder.",str(e))


g3 = rdflib.Graph()
g3.parse("./result_API_raw/page_1.ttl")
#
objectofdatabirth = """
SELECT DISTINCT ?a ?b
WHERE {
    ?a <http://schemas.delving.eu/nave/terms/creatorYearOfBirth> ?b .

}"""

qres = g3.query(objectofdatabirth)
print("this is gresssssssssssssss:", qres)
for row in qres:
    print(f"{row.a} hasObjectBirth {row.b}")
    # print("sparql done!")
