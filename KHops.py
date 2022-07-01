# KHops is used in GraphSAGE, VR-GCN, GNN-AutoScale
def GraphSAGE(g, seeds, fanouts):
    ret = []
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds))
        subg = subg.NeighborFilter('DstNode', Fn.random(fanout))
        seeds = subg.AllNodes()
        ret.append(subg)
        
    input_nodes = seeds
    return ret, input_nodes


def GraphSAGE_paper(g, seeds, fanouts):
    ret = []
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds))
        subg = subg.NeighborFilter('DstNode', Fn.random(fanout))
        seeds = subg.SrcNodes(unique=False)
        ret.append(subg)
        
    input_nodes = seeds
    return ret, input_nodes

def KHops_dgl(g, seeds, fanouts):
    ret = []
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds)).NeighborFilter('DstNode', Fn.random(fanout))
        seeds = subg.AllNodes(unique=True)
        ret.append(subg)
    return ret

def KHops_bias_dgl(g, seeds, fanouts, probs):
    ret = []
    for fanout in fanouts:
        subg = g.NodeFilter('DstNode', Fn.in(seeds))
        subg = subg.NeighborFilter('DstNode', Fn.random(fanout, probs[subg.SrcNodes(unique=False)]))
        seeds = subg.AllNodes(unique=True)
        ret.append(subg)
    return ret
