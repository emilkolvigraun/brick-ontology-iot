from rdflib import Graph, Namespace, URIRef, Literal
import rdflib, json, requests, time

RDF        = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS       = Namespace('http://www.w3.org/2000/01/rdf-schema#')
OWL        = Namespace('http://www.w3.org/2002/07/owl#')
BRICK      = Namespace('https://brickschema.org/schema/1.1.0/Brick#')

NAMESPACE = Namespace('http://ses.sdk.dk/junk/example#')

def create_model():
    graph = Graph()

    path = lambda filename: filename
    graph.parse(path('Brick_expanded.ttl'), format='turtle')
    
    graph.bind('rdf'  , RDF)
    graph.bind('rdfs' , RDFS)
    graph.bind('owl'  , OWL)
    graph.bind('brick', BRICK)
    graph.bind('n'    , NAMESPACE)
    
    return graph

def query (graph, query):
    r = graph.query(query)
    return list(map(lambda row: list(row), r))

def update (graph, query):
    r = graph.update(query)

def pprint (structure):
    pretty = json.dumps(structure, sort_keys=True, indent=4, separators=(',', ': '))
    # lol
    print(pretty)

def log(tag:str, msg:str):
    print('%s | %s : %s'%(str(time.time()), tag, msg))

