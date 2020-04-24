
class Bag(object):

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node is not None:
            yield node.val
            node = node.next_node

    def __contains__(self, item):
        tmp = self._first
        while tmp:
            if tmp == item:
                return True
        return False

    def add(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def remove(self, val):
        del_node = Node(val)
        current_node = self._first
        before_node = self._first
        while current_node is not None:
            if current_node.val == del_node.val:
                before_node.next_node = current_node.next_node
                del current_node
            else:
                before_node = current_node
                current_node = current_node.next_node
        self._size -= 1


    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

class Node(object):
    def __init__(self, val):
        self._val = val
        self.next_node = None

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, node):
        self._next_node = node

class Stack(object):

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def push(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def pop(self):
        if self._first:
            old = self._first
            self._first = self._first.next_node
            self._size -= 1
            return old.val
        return None

    def peek(self):
        if self._first:
            return self._first.val
        return None
