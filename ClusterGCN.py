partition_node = metis(g, ...)

def clustergcn(g, partition_node, seed_idxs):
    node_set = set(partition_node[seed_idxs])
    return g.NodeFilter('AllNode', Fn.in(node_set))
    