import collections

from Nodes import *
import pandas as pd
import sys


class FastestGraph:
    def __init__(self, nodesArray):
        self.graph = {}
        self.nodesArray = nodesArray

    # undirected graph
    def addEdge(self, node1, node2, speed):
        distance = nodesDistance(node1, node2, self.nodesArray)
        timeTaken = distance / (speed/3.6)

        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1].update({node2: timeTaken})

        if node2 not in self.graph:
            self.graph[node2] = {}
        self.graph[node2].update({node1: timeTaken})

    def linkAllNodes(self):
        df = pd.read_csv("linked-nodes-with-speed.csv")

        for node1, node2 , speed in zip(list(df['node1']), list(df['node2']), list(df['speed'])):
            self.addEdge(node1, node2, speed)

    def fastestPath(self, sourceNode, destinationNode):
        inf = sys.maxsize
        timeTaken = {}
        prev = {}
        unvisitedNodes = []

        # initialize distance and previous dict
        for vertex in self.graph.keys():
            timeTaken[vertex] = inf
            prev[vertex] = None
            unvisitedNodes.append(vertex)
        timeTaken[sourceNode] = 0

        # visit each node, while list is not empty
        while len(unvisitedNodes):
            currentNode = unvisitedNodes[0]
            minTimeTaken = timeTaken[currentNode]

            # find closest neighbour to currentNode to visit
            for i in unvisitedNodes:
                if timeTaken[i] < minTimeTaken:
                    currentNode = i
                    minTimeTaken = timeTaken[i]

            # remove from unvisitedNode, mark as visited
            unvisitedNodes.remove(currentNode)

            # check each neighbour linked to currentNode, update cost in distance dict
            for neighbour in self.graph[currentNode]:
                if neighbour in unvisitedNodes:
                    cost = timeTaken[currentNode] + self.graph[currentNode][neighbour]

                    if cost < timeTaken[neighbour]:
                        timeTaken[neighbour] = cost
                        prev[neighbour] = currentNode

                    # if destination already reached, break
                    # if not implemented, will continue checking for other neighbours
                    if neighbour == destinationNode:
                        break

        # backtracking of path
        # pathing from node to node 1->2->3
        path = []
        path.append(destinationNode)
        temp = prev[destinationNode]

        while temp is not None:
            path.append(temp)
            temp = prev[temp]

        path.reverse()
        print(path)

        # pathing coordinates, array of (lat, long) from start to end destination
        pathingCoords = []

        for i in path:
            pathingCoords.append((self.nodesArray[i].latitude, self.nodesArray[i].longitude))

        return pathingCoords

    def print(self):
        print(self.graph)
