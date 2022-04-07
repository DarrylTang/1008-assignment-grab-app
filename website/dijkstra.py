from .Nodes import *
import pandas as pd
import sys

class Graph:
    def __init__(self, nodesArray):
        self.graph = {}
        self.nodesArray = nodesArray

    #undirected graph
    def addEdge(self, node1, node2):
        distance = nodesDistance(node1, node2, self.nodesArray)

        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1].update({node2:distance})

        if node2 not in self.graph:
            self.graph[node2] = {}
        self.graph[node2].update({node1:distance})

    def linkAllNodes(self):
        df = pd.read_csv("./website/linked-nodes.csv")

        for node1, node2 in zip(list(df['node1']), list(df['node2'])):
            self.addEdge(node1, node2)

    def dijkstraAlgoGetPath(self, sourceNode, destinationNode):
        inf = sys.maxsize
        distance = {}
        prev = {}
        unvisitedNodes = []

        #initialize distance and previous dict
        for vertex in self.graph.keys():
            distance[vertex] = inf
            prev[vertex] = None
            unvisitedNodes.append(vertex)
        distance[sourceNode] = 0

        #visit each node, while list is not empty
        while len(unvisitedNodes):
            currentNode = unvisitedNodes[0]
            minDist = distance[currentNode]
            
            #find closest neighbour to currentNode to visit
            for i in unvisitedNodes:
                if distance[i] < minDist:
                    currentNode = i
                    minDist = distance[i]

            #remove from unvisitedNode, mark as visited
            unvisitedNodes.remove(currentNode)

            #check each neighbour linked to currentNode, update cost in distance dict
            for neighbour in self.graph[currentNode]:
                if neighbour in unvisitedNodes:
                    cost = distance[currentNode] + self.graph[currentNode][neighbour]

                    if cost < distance[neighbour]:
                        distance[neighbour] = cost
                        prev[neighbour] = currentNode

                    #if destination already reached, break
                    #if not implemented, will continue checking for other neighbours
                    if neighbour == destinationNode:
                        break

        #backtracking of path
        #pathing from node to node 1->2->3
        path = []
        path.append(destinationNode)   
        temp = prev[destinationNode]

        while temp is not None:
            path.append(temp)
            temp = prev[temp]

        path.reverse()
        # print(path)

        #pathing coordinates, array of (lat, long) from start to end destination
        pathingCoords = []

        for i in path:
            pathingCoords.append([self.nodesArray[i].latitude, self.nodesArray[i].longitude])

        totalDistance = distance[destinationNode]

        return pathingCoords, totalDistance

    def print(self):
        print(self.graph)

