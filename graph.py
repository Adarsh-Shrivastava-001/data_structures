#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 22:55:49 2019

@author: adarsh
"""


class Graph:
    
    # n is number of nodes
    # adj_mat = 1 means graph will be represented internally as adjacency matrix
    # if adj_mat = 0 , graph will be represented as a collection of linked lists
    
    
    def __init__(self, n, adj_mat=1, draw_graph=False):
        
        """key components of graph"""
        
        self.n=n                    # number of nodes
        self.is_adj_mat=adj_mat     # type of internal representation
        self.__adj_mat=None
        self.__lin_list=None
        self.draw_graph=draw_graph
        
        """ components required for Weighted Union Find with Path Compression Algorithm"""
        
        self.__root=[i for i in range(self.n)]    # entry at ith position gives the position of root of ith node
        self.__weight=[1 for i in range(self.n)]  # weight array for self.__root : entry at ith index represents number of nodes with root as ith node
        
        
        if self.is_adj_mat==True:
            # initialising adjacency matrix
            self.__adj_mat=[[0 for i in range(n)] for j in range(n)]
        else:
            # initialising Linked list
            self.__lin_list=[[] for i in range(n)]
            
        # if draw_graph is set to true it will lead to many extra steps which would be required for drwaing the graph
        # also it needs many external dependencies
            
        if draw_graph==True:
            # make necessary imports
            global nx, pgv, nxpd
            nx=__import__('networkx', globals(),locals())
            pgv=__import__('pygraphviz', globals(),locals())
            nxpd=__import__('nxpd', globals(),locals())            
            nxpd.nxpdParams['show'] = 'ipynb'          
            
            self.actions=[] #seems unnecessary will be removed in future
            self.__edges=[] # stores the record of all edges in form (node1, node2)
            self.graph=nx.Graph()
            for i in range(n):
                self.graph.add_node(i)
            
    def root(self,node):
        # finding root of the given node         
        if self.__root[node]==node:
            return node
        return self.root(self.__root[node])
        
        
        
    def add_edge(self, node1, node2): 
        # Adding an undirected edge between node1 and node2
    
        if self.is_adj_mat==True:
            self.__adj_mat[node1][node2]=1
            self.__adj_mat[node2][node1]=1
        else:
            self.__lin_list[node1].append(node2)
            self.__lin_list[node2].append(node1)
        
        
        root1=self.root(node1)  # checking root of node1
        root2=self.root(node2)  # checking root of node2
        if root1!=root2:
            # if they are not equal than node1 and node 2 are disconnected
            if self.__weight[root1]>self.__weight[root2]:
                # if root1 has larger tree than add tree2 to tree1
                self.__weight[root1]+=self.__weight[root2]
                self.__root[root2]=self.__root[root1]
                
            else:
                # if root2 has larger tree then add tree1 to tree2
                self.__weight[root2]+=self.__weight[root1]
                self.__root[root1]=self.__root[root2]              
                
        if self.draw_graph==True:
            self.actions.append('Added edge : '+ str(node1)+'-'+str(node2))
            self.__edges.append([node1,node2])
            self.graph.add_edge(node1,node2)    
            self.__edges.append([node2,node1])
            self.graph.add_edge(node2,node1)
                        
            
            
    def connected_to(self, node):
        # returns a list of nodes directly connected to the given node
        connections=[]
        if self.is_adj_mat==True:
            for i in range(self.n):
                if self.__adj_mat[node][i]==1:
                    connections.append(i)
        else:
            connections=self.__lin_list[node]
        
        return connections
                
    def bfs(self, node):
        # prints the breadth first traversal of graph
        qu=[node]   # queue for implimenting bfs
        visited=[0 for i in range(self.n)]
        visited[node]=1
        front=0
        
        while front < len(qu):
            neigh=self.connected_to(qu[front])  # extracting all the nodes connected to the first node in queue
            for i in neigh:
                if visited[i]==0:
                    qu.append(i)
                    visited[i]=1
            print(qu[front])
            
            front=front + 1
            
    def dfs(self, node):
        # prints the depth first traversal of graph
        stk=[node] # maintaining stack for implimenting dfs
        visited=[0 for i in range(self.n)]  # if node is visited then its is marked 1 else 0
        visited[node]=1
        top=0
        print(node)        
        
        while top>=0:
            neigh=self.connected_to(stk[top])
            if neigh==[]:
                top=top-1
            for i in neigh:
                f=0 # flag constant to kepp track of whether or not we found a neighbour to be appended
                # if any of the neighbour is unvisited append it to stack and carry out necessary operations
                if visited[i]==0:
                    stk.append(i)
                    top=top+1
                    visited[i]=1
                    print(i)
                    f=1
                    break
                if f==0 and i==neigh[-1]:   #if no such neighbour is left we pop the item from stack
                    top=top-1
                    
        
    def draw(self):
        return nxpd.draw(self.graph)
    
    def is_connected(self,node1, node2):
        # returns boolean value
        # True if node1 is connected to node2
        # else False
        if self.root(node1)==self.root(node2):
            return True
        else:
            return False
        
    def connected_components(self):
        # return the number of connected components in a graph
        # the number of connected components will be eaqual to the number of roots in the graph
        num=0
        for i in range(self.n):
            if i==self.__root[i]:
                num=num+1
        return num
    
    def num_nodes(self, node):
        # this function returns the number of node connected to given node
        # this is O(1) operation as opposed to connected_to function which is O(n)
        return self.__weight[self.root(node)]
    
    
             
                
        
a=Graph(10, 1, draw_graph=True)

a.add_edge(1,2)
a.add_edge(2,3)
a.add_edge(3,4)
a.add_edge(4,5)
a.add_edge(4,2)
a.add_edge(2,6)
a.add_edge(2,7)
a.add_edge(0,8)