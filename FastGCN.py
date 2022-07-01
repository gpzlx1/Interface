def FastGCN(g, seeds, fanouts):
    ret = []
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds))
        subg = subg.NodeFilter('SrcNodes', Fn.random(fanout))
        ret.append(subg)
        seeds = subg.AllNodes()
    return ret


def FastGCN_bias(g, seeds, fanouts, probs):
    ret = []
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds))
        probs = probs[subg.SrcNodes(unique=True)]
        # normalize maybe?
        subg = subg.NodeFilter('SrcNodes', Fn.random(fanout, probs))
        seeds = subg.AllNodes()
        ret.append(subg)
    return ret