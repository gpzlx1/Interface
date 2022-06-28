def shadow_gnn(g, seeds, fanouts):
    ret = set()
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds)).NeighborFilter('DstNode', Fn.random(fanout))
        seeds = subg.AllNodes()
        ret.insert(seeds)

    ret_g = g.nodeFilter('AllNodes', Fn.in(ret))
    return ret_g