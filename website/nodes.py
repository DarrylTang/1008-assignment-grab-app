import geopandas as gpd
from haversine import haversine, Unit

class Node:
    def __init__(self, nodeNum, latitude, longitude):
        self.nodeNum = nodeNum
        self.latitude = latitude
        self.longitude = longitude

#read nodes.geojson and populate doubly linked list
def getNodesArray():
    filename = "./website/nodes.geojson"
    data = gpd.read_file(filename)

    nodesArray = [0 for x in range(len(data))]

    for i in range(len(data)):
        nodeNum = data["node"][i]
        longitude = data["geometry"][i].x
        latitude = data["geometry"][i].y
        newNode = Node(nodeNum, latitude, longitude)
        nodesArray[newNode.nodeNum] = newNode

    return nodesArray

#gets distance between 2 nodes
#default returns distance in km
def nodesDistance(node1, node2, nodesArray):
    loc1 = (nodesArray[node1].latitude, nodesArray[node1].longitude)
    loc2 = (nodesArray[node2].latitude, nodesArray[node2].longitude)

    #distance = haversine(loc1, loc2)
    distance = haversine(loc1, loc2, unit=Unit.METERS)

    return distance
