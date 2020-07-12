import time
import random
import numpy as np
from scipy.sparse import lil_matrix

class KeyValueBSTNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def add_data(self, new_node):
        if not self.key:
            self.key = new_node.key
            self.value = new_node.value
        elif new_node.key == self.key:
            self.value = new_node.value
        elif new_node.key > self.key:
            if self.right:
                self.right.add_data(new_node.key, new_node.value)
            else:
                self.right = KeyValueBSTNode(new_node.key, new_node.value)
        else:
            if self.left:
                self.left.add_data(new_node.key, new_node.value)
            else:
                self.left = KeyValueBSTNode(new_node.key, new_node.value)

    def add_data(self, new_key, new_value):
        if not self.key:
            self.key = new_key
            self.value = new_value
        elif new_key == self.key:
            self.value = new_value
        elif new_key > self.key:
            if self.right:
                self.right.add_data(new_key, new_value)
            else:
                self.right = KeyValueBSTNode(new_key, new_value)
        else:
            if self.left:
                self.left.add_data(new_key, new_value)
            else:
                self.left = KeyValueBSTNode(new_key, new_value)

    def get_data(self, key):
        if key == self.key:
            return self.value
        elif key < self.key:
            if self.left:
                return self.left.get_data(key)
            else:
                return None
        else:
            if self.right:
                return self.right.get_data(key)
            else:
                return None

    def get_ordered_children(self):
        ordered_children = []

        if self.left:
            ordered_children += self.left.get_ordered_children()
        ordered_children.append(self)
        if self.right:
            ordered_children += self.right.get_ordered_children()

        return ordered_children

    def get_num_of_children(self):
        children_sum = 1 # me

        if self.left:
            sum += self.left.get_num_of_children()
        if self.right:
            sum += self.right.get_num_of_children()
        return children_sum

    def print_children(self):
        if self.left:
            print('(', end='')
            self.left.print_children()
            print(') <- ', end='')
        print(f'{self.key}, {self.value}', end='')
        if self.right:
            print(' -> (', end='')
            self.right.print_children()
            print(')', end='')


class KeyValueBST:
    def __init__(self, data_list = None, cache_size=0, balance_after_ops=0):
        self.root = None

        if data_list:
            self.add(data_list)

    def add_node(self, new_data):
        if isinstance(new_data, list):
            for element in new_data:
                if self.root:
                    self.root.add_data(element.key, element.value)
                else:
                    self.root = KeyValueBSTNode(element.key, element.value)
        elif isinstance(new_data, KeyValueBST):
            if new_data.root:
                for element in new_data.root.get_ordered_children():
                    if self.root:
                        self.root.add_data(element.key, element.value)
                    else:
                        self.root = KeyValueBSTNode(element.key, element.value)
        else:
            if self.root:
                self.root.add_data(new_data.key, new_data.value)
            else:
                self.root = KeyValueBSTNode(new_data.key, new_data.value)

    def add(self, new_key, new_value):
        if self.root:
            self.root.add_data(new_key, new_value)
        else:
            self.root = KeyValueBSTNode(new_key, new_value)

    def find(self, key):
        # TODO: check cache
        if self.root:
            return self.root.get_data(key)
        else:
            return None

    # builds node tree manually using a recursive function that subdivides vals into smaller and smaller branches
    def balance_new_tree(self, vals, start_of_tree, end_of_tree):
        # check the tree to subdivide is not zero
        if start_of_tree > end_of_tree: # floored division + not changing one bounds at a time makes it only ever go over
            return None

        # create center of new subdivide
        new_root_index = (end_of_tree + start_of_tree) // 2 # NOTE: floored division
        #print(f'new root: {str(vals[new_root_index])}')
        new_root = KeyValueBSTNode(vals[new_root_index].key, vals[new_root_index].value)

        # split build left and right side of new tree using this function
        new_root.left = self.balance_new_tree(vals, start_of_tree, new_root_index - 1)
        new_root.right = self.balance_new_tree(vals, new_root_index + 1, end_of_tree)

        return new_root

    def balance(self):
        if self.root:
            ordered_vals = self.root.get_ordered_children()
            self.root = self.balance_new_tree(ordered_vals, 0, len(ordered_vals) - 1)


    def print_ascii(self):
        if self.root:
            self.root.print_children()
            print('')
        else:
            print('empty')

    def __add__(self, other):
        # TODO: make smart balance
        bst_sum = KeyValueBST()
        bst_sum.add_node(self)
        bst_sum.add_node(other)
        return bst_sum

class BigSparseMatrix:
    kv_map = KeyValueBST()
    rows = 0
    cols = 0

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def getrow(self, row):
        if 0 <= row < self.rows:
            found_row = self.kv_map.find(row)
            if found_row:
                return found_row
            else:
                return [0.0] * self.cols
        else:
            raise IndexError

    def __getitem__(self, key):
        if isinstance(key, int) == 1:
            # get row
            if 0 <= key < self.rows:
                found_row = self.kv_map.find(key)
                if found_row:
                    return found_row
                else:
                    return [0.0] * self.cols
            else:
                raise IndexError
        elif type(key) is tuple and len(key) == 2:
            # get row, col value
            row, col = key
            if 0 <= row < self.rows:
                if 0 <= col < self.cols:
                    found_row = self.kv_map.find(row)
                    if found_row:
                        return found_row[col]
                    else:
                        return 0.0
                else:
                    raise IndexError
            else:
                raise IndexError
        else:
            raise IndexError

    def __setitem__(self, key, value):
        if isinstance(key, int) == 1:
            # get row
            if 0 <= key < self.rows:
                if len(value) == self.cols:
                    self.kv_map.add(key, value)
                else:
                    raise ValueError
            else:
                raise IndexError
        elif type(key) is tuple and len(key) == 2:
            # get row, col value
            row, col = key
            if 0 <= row < self.rows:
                if 0 <= col < self.cols:
                    found_row = self.kv_map.find(row)
                    if found_row:
                        found_row[col] = value
                    else:
                        new_row = [0.0] * self.cols
                        new_row[col] = value
                        self.kv_map.add(row, new_row)
                else:
                    raise IndexError
            else:
                raise IndexError
        else:
            raise IndexError
