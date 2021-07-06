import requests

def connectToGraphDB(query):
    # response = requests.get('http://192.168.200.8:7200/repositories/subject_ontology',
    #              params=query, headers={'Accept': 'application/sparql-results+json'}, )
    response = requests.get('http://localhost:7200/repositories/SubjectOntologyVersion16',
                  params=query, headers={'Accept': 'application/sparql-results+json'}, )
    return response

def updateToGraphDB(update):
    response = requests.post('http://localhost:7200/repositories/SubjectOntologyVersion16/statements',
                            params=update, headers={'Accept': 'application/sparql-results+json'}, )
    return response