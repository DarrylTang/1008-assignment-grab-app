from .nodes import *
import pandas as pd
import sys
class Graph:
    def __init__(self, nodesArray):
        self.graph = {}
        self.nodesArray = nodesArray

    #undirected graph
    def addEdge(self, node1, node2, speed):
        cost = nodesDistance(node1, node2, self.nodesArray)

        if speed:
            #speed stored is in km/h
            #distance is in metres
            #divided by 3.6 to convert to m/s
            #timetaken is in seconds
            cost = cost / (speed/3.6)

        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1].update({node2:cost})

        if node2 not in self.graph:
            self.graph[node2] = {}
        self.graph[node2].update({node1:cost})

    def linkAllNodes(self, speedGraph):
        df = pd.read_csv("./website/linked-nodes.csv")

        if not speedGraph: 
            for node1, node2 in zip(list(df['node1']), list(df['node2'])):
                self.addEdge(node1, node2, None)
        else:
            for node1, node2, speed in zip(list(df['node1']), list(df['node2']), list(df['speed'])):
                self.addEdge(node1, node2, speed)

    def dijkstraAlgoGetPath(self, sourceNode, destinationNode):
        inf = sys.maxsize
        distanceOrTime = {}
        prev = {}
        unvisitedNodes = []

        #initialize distance and previous dict
        for vertex in self.graph.keys():
            distanceOrTime[vertex] = inf
            prev[vertex] = None
            unvisitedNodes.append(vertex)
        distanceOrTime[sourceNode] = 0

        #visit each node, while list is not empty
        while len(unvisitedNodes):
            currentNode = unvisitedNodes[0]
            minDist = distanceOrTime[currentNode]
            
            #find closest neighbour to currentNode to visit
            for i in unvisitedNodes:
                if distanceOrTime[i] < minDist:
                    currentNode = i
                    minDist = distanceOrTime[i]

            #remove from unvisitedNode, mark as visited
            unvisitedNodes.remove(currentNode)

            #check each neighbour linked to currentNode, update cost in distance dict
            for neighbour in self.graph[currentNode]:
                if neighbour in unvisitedNodes:
                    cost = distanceOrTime[currentNode] + self.graph[currentNode][neighbour]

                    if cost < distanceOrTime[neighbour]:
                        distanceOrTime[neighbour] = cost
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

        #pathing coordinates, array of (lat, long) from start to end destination
        pathingCoords = []

        for i in path:
            pathingCoords.append([self.nodesArray[i].latitude, self.nodesArray[i].longitude])

        # cost here refers to either time or distance depending on self.graph
        # two types of graph can be created, nodes with speed or nodes with distance graph
        # returned value distance is in metres
        # returned value time is in seconds
        totalCost = distanceOrTime[destinationNode]

        return pathingCoords, totalCost

    def print(self):
        print(self.graph)