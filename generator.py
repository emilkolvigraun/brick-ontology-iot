from uuid import uuid4
import pandas
from model import *

TTL_FILENAME = 'boards.ttl'

data = pandas.read_csv('dataplot/converted.csv')

graph = create_model()

# define the board, and add its rdf term as "thing"
board = NAMESPACE['/board']
graph.add((board, RDF.type, BRICK['Thing']))

# define sensor, and add its rdf term as "sensor"
sensor = NAMESPACE['/board/sensor']
graph.add((sensor, RDF.type, BRICK['Sensor']))

# configure relation and property
graph.add((board, NAMESPACE.hasA, sensor))
graph.add((board, NAMESPACE.chip, Literal('esp32')))

# define a specific type of sensor, the temperature sensor
temperature = NAMESPACE['board/sensor/temperature']
graph.add((temperature, RDF.subClassOf, BRICK['Sensor']))
graph.add((temperature, NAMESPACE.isA, Literal('mcp9700')))
graph.add((temperature, NAMESPACE.minValue, Literal(0)))
graph.add((temperature, NAMESPACE.maxValue, Literal(200)))
graph.add((temperature, NAMESPACE.rawValues, Literal(data['truth'])))
graph.add((temperature, NAMESPACE.convertedValues, Literal([i for i in data.calculated])))

# define conversion namespace
conversion  = NAMESPACE['board/sensor/temperature/conversion']
graph.add((conversion, RDF.type, BRICK['Thing']))
graph.add((conversion, RDF.subClassOf, BRICK['Thing']))
graph.add((conversion, NAMESPACE.isDefinedBy, temperature))
graph.add((conversion, NAMESPACE.formula, Literal('y = 0.05253585325722113*(x-1452.0035211267605)+23.2')))

graph.serialize(TTL_FILENAME, 'turtle')

del graph
graph = Graph()
graph.parse(TTL_FILENAME, format='turtle')


board_query = \
'''
SELECT DISTINCT ?sensor_model ?min_val ?max_val ?converted ?con_formula
WHERE {
    ?temperature     rdf:subClassOf brick:Sensor .
    ?conversion      rdf:type/rdf:subClassOf* brick:Thing .
    
    ?temperature     n:isA ?sensor_model .
    ?temperature     n:minValue ?min_val .
    ?temperature     n:maxValue ?max_val .
    ?conversion      n:formula ?con_formula .
    ?temperature     n:convertedValues ?converted .
}
'''
pprint(query(graph, board_query))
