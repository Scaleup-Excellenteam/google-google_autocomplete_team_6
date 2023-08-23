# coding: utf-8


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.data_list = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, data=None):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        if node.data_list:
            node.data_list.append(data)
        else:
            node.data_list = [data]

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return []
            node = node.children[char]
        if node.is_end_of_word:
            return node.data_list
        return []
