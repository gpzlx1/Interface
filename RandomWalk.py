def random_walk(g, seeds, depth): 
    ret = []
    for I in range(depth):
        subg = g.NodeFilter('DstNode', Fn.in(seeds))
        subg = subg.NeighborFilter('DstNode', Fn.random(1, replace=False), keep_dim=True)
        seeds = subg.SrcNodes(Unique=False)
        ret.append(seeds)
    return ret 
