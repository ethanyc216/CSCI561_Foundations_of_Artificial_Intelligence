#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

############################
##   CSCI 561 Fall 2019   ##
##       Homework 1       ##
##       Yifan Chen       ##
##  ethanyc216@gmail.com  ##
############################

# util supports to homework

import heapq

class Stack:
    """
      A container with a last-in-first-out (LIFO) queuing policy.
    """
    def __init__(self):
        self.list = []

    def push(self,item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

class Queue:
    """
      A container with a first-in-first-out (FIFO) queuing policy.
    """
    def __init__(self):
        self.list = []

    def push(self,item):
        self.list.insert(0,item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)



