def random_walk(g, seeds, depth): 
    ret = []
    for I in range(depth):
        subg = g.NodeFilter('DstNode', Fn.in(seeds)).NeighborFilter('DstNode' Fn.random(1, replace=False))
        seeds = subg.SrcNodes(Unique=False)
        ret.append(seeds)
    return ret 
