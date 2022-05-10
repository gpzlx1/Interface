import interface as F


def graphsage_sampler(Graph, num_picks, seeds):

    # get seeds' neighbors
    subg = F.Filter_by_choice(Graph, seeds, 'node.dstnode')

    # Sample
    subg = F.Sample_neigh(subg, num_picks, None, 'P', False)

    return subg


def random_walk(Graph, seeds, length):
    ret = [seeds]
    root = seeds
    for _ in range(length):
        # Get Neigh
        subg = F.Filter_by_choice(Graph, root, 'node.dstnode')
        # Sample
        subg = F.Sample_neigh(subg, 1, None, 'P', False)
        # next layer
        root = F.Query(subg, 'node.srcnode')
        ret.append(root)
    return ret

