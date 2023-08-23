# coding: utf-8


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.data = None  # can be used to store metadata for a word

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
        node.data = data

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        if node.is_end_of_word:
            return node.data
        return None
