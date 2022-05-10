import interface as F


def ladies_sampler(Graph, num_budget, seeds, node_probs):
    
    # get seeds' neighbors
    subg = F.Filter_by_choice(Graph, seeds, 'node.dstnode') 

    # compute probs
    subg_reverse = subg.reverse()
    probs = node_probs[F.Query(subg_reverse, 'edge.srcnode')]
    probs = F.SpMM(subg_reverse, probs, 'sum')
    probs = probs * probs / probs.sum()

    # Sample
    candidates = F.Query(subg_reverse, 'node.dstnode')[F.Sample(num_budget, probs, 'P', False)]

    retg = F.Filter_by_choice(subg, candidates, 'node.srcnode')

    return retg # auto-relabel when return a graph or graph list, but transparently


def fastgcn_sampler(Graph, num_budget, seeds, node_probs):
    
    # get seeds' neighbors
    subg = F.Filter_by_choice(Graph, seeds, 'node.dstnode') 

    # compute probs
    srcnode = node_probs[F.Query(subg, 'node.srcnode')]
    probs = node_probs[srcnode]
    probs = probs * probs / probs.sum()

    # Sample
    candidates = srcnode[F.Sample(num_budget, probs, 'P', False)]

    retg = F.Filter_by_choice(subg, candidates, 'node.srcnode')

    return retg