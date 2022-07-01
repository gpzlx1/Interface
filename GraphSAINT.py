def GraphSaint(g, seeds, depth):
    node_set = set()
    node_set.insert(seeds)
    for _ in depth:
        subg = g.NodeFilter('DstNode', Fn.in(seeds))
        subg = subg.NeighborFilter('DstNode', Fn.random(1, replace=False))
        seeds = subg.SrcNodes(unique=False)
        node_set.insert(seeds)

    return g.NodeFilter('AllNode', Fn.in(node_set))
