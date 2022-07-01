def LADIES(g, seeds, fanouts, weight):
    ret = []
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds))
        probs = SpMM('SrcNode', weight[subg.DstNode(unique=False)], 'Sum')
        subg = subg.NodeFilter('SrcNodes', Fn.random(fanout, probs))
        ret.append(subg)
        seeds = subg.AllNodes()
    return ret