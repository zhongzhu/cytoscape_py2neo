# coding=utf-8
from flask import Flask
from flask.ext.jsonpify import jsonify
from py2neo import Graph

app = Flask(__name__)
graph = Graph()

def buildNodes(aNodeRecord):
    data = {"id": str(aNodeRecord.n._id)}
    data.update(aNodeRecord.n.properties)

    labelSet = aNodeRecord.n.labels
    if 'Movie' in labelSet:
        data.update({"name": aNodeRecord.n.properties['title'], "faveColor":"#EDA1ED"})
    elif 'Person' in labelSet:
        data.update({"faveColor":"#61bffc"})

    return {"data": data}

def buildEdges(aRelationRecord):
    data = {"source": str(aRelationRecord.r.start_node._id), 
      "target": str(aRelationRecord.r.end_node._id),
      "relationship": aRelationRecord.r.rel.type}

    return {"data": data}

def getGraphData():    
    nodes = map(buildNodes, graph.cypher.execute('MATCH n return n'))
    edges = map(buildEdges, graph.cypher.execute('MATCH ()-[r]->() RETURN r'))

    return {"nodes": nodes, "edges": edges}

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/haha', methods=['GET', 'POST'])
def haha():
    elements = getGraphData()

    style = [
        {
          "selector": 'node',
          "css": {
            'content': 'data(name)',
            'text-valign': 'center',
            # 'width': 'mapData(weight, 0, 100, 10, 60)',
            # 'height': 'mapData(weight, 0, 100, 10, 60)',            
            # 'color': 'white',
            'background-color': 'data(faveColor)',
            "min-zoomed-font-size": 6,
            "font-size": 6,
            # 'text-outline-width': 1,
            # 'text-outline-color': '#888'
          }
        },
        {
          "selector": 'edge',
          "css": {
              # 'curve-style': 'haystack',
              'target-arrow-shape': 'triangle',
              'content': 'data(relationship)',
              "font-size": 6,
              "min-zoomed-font-size": 6,
              # 'width': 2    
          }      
        },
        {
          "selector": ':selected',
          "css": {
              'background-color': 'black',
              'line-color': 'black',
              'target-arrow-color': 'black',
              'source-arrow-color': 'black'
          }      
        },    
        {
          "selector": '.faded',
          "css": {
              'opacity': 0.25,
              'text-opacity': 0
          }      
        },    
      ]

    return jsonify(elements = elements, style = style)    

if __name__ == '__main__':
    app.debug = True
    app.run(port=8899)