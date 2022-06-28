# KHops is used in GraphSAGE, VR-GCN, GNN-AutoScale
def KHops_origin(g, seeds, fanouts):
    ret = []
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds)).NeighborFilter('DstNode', Fn.random(fanout))
        ret.append(subg)
        seeds = subg.AllNodes(unique=False)
    return ret


def KHops_dgl(g, seeds, fanouts):
    ret = []
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds)).NeighborFilter('DstNode', Fn.random(fanout))
        ret.append(subg)
        seeds = subg.AllNodes(unique=True)
    return ret

# ?? question 1 : the reference about subg.DstData
# ?? question 2 : the relation between AllData, DstData, SrcData
#g.DstData['w'] = bias
def KHops_bias_dgl(g, seeds, fanouts, probs):
    ret = []
    for fanout in fanouts:
        #subg = g.NodeFilter('DstNode', Fn.in(seeds)).NeighborFilter('DstNode', Fn.random(fanout, g.SrcData['w']))
        subg = g.NodeFilter('DstNode', Fn.in(seeds))
        subg = g.NeighborFilter('DstNode', Fn.random(fanout, probs[subg.SrcNodes(unique=False)]))
        ret.append(subg)
        seeds = subg.AllNodes(unique=True)
    return ret
