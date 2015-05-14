from py2neo import Graph

graph = Graph()

def buildNodes(aNodeRecord):
    data = {"id": aNodeRecord.n._id}
    data.update(aNodeRecord.n.properties)

    return {"data": data}

def buildRelations(aRelationRecord):
    data = {"source": aRelationRecord.r.start_node._id, "target": aRelationRecord.r.end_node._id}


def getGraphData():    
    # elements["nodes"].append({"data": {"id": rrh_id, "name": type + rrh_name, "faveColor":"#EDA1ED", "weight":30}})
    # elements["edges"].append({"data": {"source": enb_id, "target": rrh_id, "weight":5}}) 

    nodeRecords = graph.cypher.execute('MATCH n return n')
    print(nodeRecords)

    nodes = map(buildNodes, nodeRecords)
    print(nodes)

    relationRecords = graph.cypher.execute('MATCH ()-[r]->() RETURN r')
    relations = map(buildRelations, relationRecords)

    elements = {"nodes": nodes, "edges": relations}

    return elements

getGraphData()