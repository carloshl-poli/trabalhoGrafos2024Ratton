import numpy as np

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.parent = 0
        self.level = 0

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self, data, level = 0, parent = 0):
        new_node = Node(data)
        new_node.parent = parent
        new_node.level = level
        self.size += 1
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
    
    def dequeue(self, dequeue_node = False):
        if self.is_empty():
            raise IndexError("Queue is empty")
        temp = self.front
        self.front = temp.next
        self.size -= 1
        if self.front is None:
            self.rear = None
        if dequeue_node: return temp
        return temp.data
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.front.data


class Stack:
    def __init__(self):
        self.top = None
    
    def is_empty(self):
        return self.top is None
    
    def push(self, data, level = 0, parent = 0):
        new_node = Node(data)
        new_node.parent = parent
        new_node.level = level
        new_node.next = self.top
        self.top = new_node
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        temp = self.top
        self.top = self.top.next
        return temp.data
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.top.data


class LinkedList:
    def __init__(self):
        self.head = None
    
    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
    
    def delete(self, key):
        current = self.head
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        if not current:
            return  # Elemento não encontrado
        if not prev:  # O elemento a ser removido é o primeiro
            self.head = current.next
        else:
            prev.next = current.next

    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                return current
            current = current.next
        return None
    
    def insert_sorted(self, data):
        """Insere um novo nó na lista de forma ordenada."""
        new_node = Node(data)
        if not self.head or self.head.data >= new_node.data:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.data < new_node.data:
                current = current.next
            new_node.next = current.next
            current.next = new_node
    
    def display(self):
        current = self.head
        while current:
            print(current.data, end=' -> ')
            current = current.next
        print('None')


class SubgraphNode:
    def __init__(self, size, edges):
        self.size = size
        self.edges = edges
    
    @staticmethod
    def sort_nodes(node_array):
        return sorted(node_array, key=lambda node: node.size, reverse=True)
    