from nltk.tree import Tree

def get_lca_length(location1, location2):
    i = 0
    while i < len(location1) and i < len(location2) and location1[i] == location2[i]:
        i+=1
    return i

def get_labels_from_lca(ptree, lca_len, location):
    labels = []
    for i in range(lca_len, len(location)):
        labels.append(ptree[location[:i]].label())
    return labels

def findPath(ptree, text1, text2):
    leaf_values = ptree.leaves()
    leaf_index1 = leaf_values.index(text1)
    leaf_index2 = leaf_values.index(text2)

    location1 = ptree.leaf_treeposition(leaf_index1)
    location2 = ptree.leaf_treeposition(leaf_index2)

    #find length of least common ancestor (lca)
    lca_len = get_lca_length(location1, location2)

    #find path from the node1 to lca

    labels1 = get_labels_from_lca(ptree, lca_len, location1)
    #ignore the first element, because it will be counted in the second part of the path
    result = labels1[1:]
    #inverse, because we want to go from the node to least common ancestor
    result = result[::-1]

    #add path from lca to node2
    result = result + get_labels_from_lca(ptree, lca_len, location2)
    return result

ptree = Tree.fromstring("(VP (VERB saw) (NP (DET the) (NOUN dog)))")
print(ptree.pretty_print())
print(findPath(ptree, 'the', "dog"))

