
class TrieNode:

    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):

        node = self.root

        for character in word:

            if character not in node.children:
                node.children[character] = TrieNode()

            node = node.children[character]

        node.is_end_of_word = True

    def search_prefix(self, prefix):

        node = self.root

        for character in prefix:

            if character not in node.children:
                return []

            node = node.children[character]

        results = []

        self.collect_words(node, prefix, results)

        return results

    def collect_words(self, node, current_word, results):

        if node.is_end_of_word:
            results.append(current_word)

        for character, child_node in node.children.items():

            self.collect_words(
                child_node,
                current_word + character,
                results
            )
