import interface as F
import torch

# implementation
def graphsaint_sampler(Graph, seeds):

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

    node_list = random_walk(Graph, seeds, 5)
    node = torch.cat(node_list, dim = 0).unique()

    # node subgraph
    subg = F.Filter_by_choice(Graph, node, 'node')

    return subg

