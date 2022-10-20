# OAI-PMH:

Collecting  RDF/XML entities and converting to turtle and N-triple,

## Requirements

Install required libraries using following command before running script. pip install -r requirements.txt

## Usage

Find your python path on your system :

python = "C:\Program Files\Python37\python.exe"

#### Help:

`python path oai-pmh.py -h`

#### Test with defaults API and datasets(mauritshuis and museum-de-fundatie):

`python oai-pmh.py` 

### 1- Collect dataset from single OAI-PMH API: 

`python oai-pmh.py -u "url_base_path" -e entity`

For example: 

`python oai-pmh.py -u "https://www.collectienederland.nl/api/oai-pmh/?verb=ListRecords&metadataPrefix=edm-strict&set=" -e mauritshuis`

`python oai-pmh.py -u "https://www.collectienederland.nl/api/oai-pmh/?verb=ListRecords&metadataPrefix=edm-strict&set=" -e van-abbe-museum`

`python oai-pmh.py -e mauritshuis`

### 2- Collect datasets from multiple OAI-PMH API

add url base and entities in code(oai-pmh.py) and run codes in commandline:

`python oai-pmh.py -de `

or

`python oai-pmh.py`

### Folders after running script:

1- collected: xml/rdf

2- xml-integrate

3- converted: N-triple and turtle files

If you want to harvest new API store the folders in a separate folder because in each run the folders and files are regenerated.





