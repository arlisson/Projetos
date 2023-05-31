
from ctypes import pointer
from signal import raise_signal
from node import node


class Linked_List:

    def __init__(self):

        self.head = None
        self._size = 0

    def append(self, element):
        # inserção quando a lista já possui elementos
        if self.head:
            pointer = self.head

            while(pointer.next):
                pointer = pointer.next
            pointer.next = node(element)
        else:
            # primeira inserção
            self.head = node(element)
        self._size = self._size + 1

    # função especial len
    def __len__(self):
        return self._size

    def __getitem__(self, index):
        pointer = self.head

        for _ in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError("list index out of range1")

        if pointer:
            return pointer.data

        raise IndexError("list index out of range2")

    def __setitem__(self, index, elem):
        for _ in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError("list index out of range")

        if pointer:
            pointer.data = elem
        else:
            return IndexError("list index out of range")

    def index(self, elem):
        pointer = self.head
        i = 0
        while(pointer):
            if pointer.data == elem:
                return i
            pointer = pointer.next
            i = i+1

        raise ValueError("{} is not in list".format(elem))
