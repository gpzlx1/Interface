import torch


# Basic API
def Query(Graph, target : str):
    """Get node/edge/matrix from Graph

    Args:
        Graph (Graph): 
        target (str): Objects of operation, should be in 
            ['node', 'node.srcnode', 'node.dstnode', 
            'edge', 'edge.srcnode', 'edge,dstnode',
            'coo', 'csr']
            if target == 'node', return Graph's nodes;
            if target == 'node.srcnode', return Graph's srcnodes;
            if target == 'node.dstnode', return Graph's dstnodes;
            if target == 'edge', return Graph's eids;
            if tagget == 'edge.srcnode', return each edge's srcnode (it's also srcnode, but without dedup);
            if tagget == 'edge.dstnode', return each edge's dstnode (it's also dstnode, but without dedup);
            if target == 'coo' or 'csr', return sparse matrix;

    Returns:
        tensor or tensor list
            
    """
    pass

def Filter_by_choice(Graph, choice : torch.Tensor, target : str):
    """Filter Graph, just keep the choice data in Graph

    Args:
        Graph (Graph): 
        choice (torch.Tensor): Data you want to retain. choice.shape should be equal to Query(Graph, target).shape
        target (str): Objects of operation, should be in 
            ['node', 'node.srcnode', 'node.dstnode', 'edge']

    Returns:
        Graph: Graph after filtering

    Example:
        # node subgraph;
        # it's equal to Filter_by_choice(Graph, choice, 'node.dstnode') + Filter_by_choice(Graph, choice, 'node.srcnode')
        Filter_by_choice(Graph, choice, 'node') 

        Filter_by_choice(Graph, choice, 'node.srcnode')  
        
        # get choice's neighbors
        Filter_by_choice(Graph, choice, 'node.dstnode') 

        # edge subgraph
        Filter_by_choice(Graph, choice, 'edge') 
    """
    pass

def Filter_by_flag(Graph, flag : torch.Tensor, target : str):
    """Filter Graph by flag. Similar to filter, but more flexible.

    Args:
        Graph (Graph): 
        flag (torch.Tensor): flag data used to filter. It should be able to be converted to bool. 
            flag.shape should be equal to Query(Graph, target).shape
        target (str): Objects of operation, should be in 
            ['node', 'node.srcnode', 'node.dstnode', 
            'edge', 'edge.srcnode', 'edge,dstnode']

    Returns:
        Graph: Graph after filtering
    """
    pass

def Sample_neigh(Graph, num_pick, data : torch.Tensor, method : str, replace : bool):
    """Sample Graph's neighbors

    Args:
        Graph (Graph): 
        num_pick (int): sample how many neighbors for each dstnode
        data (torch.Tensor): probability, the shape should be equal to Query(Graph, 'node.srcnode').shape.
        method (str): 'P' or 'TopK'.
        replace (bool): wheather w/o replacement.

    Returns:
        Graph: Graph after being sampled
    """
    pass

def Sample(num_pick, data : torch.Tensor, method : str, replace : bool):
    """Sample data; return index tensor for selected data.

    Args:
        num_pick (int): sample how many numbers
        data (torch.Tensor): probability.
        method (str):  'P' or 'TopK'.
        replace (bool): wheather w/o replacement.

    Returns:
        torch.Tensor: index tensor for selected data.
    """
    pass

def CGraph(format : str, data_list : list):
    """Create a Graph

    Args:
        format (str): 'coo' or 'csr'
        data_list (list): tensor list

    Returns:
        Graph
    """
    pass

def Flag_scatter(src, dst, flag_value, default_value):
    """Generate Flag tensor. if dst in src, the flag of dst will be flag_value; otherwise it will be default_value;

    Args:
        src (torch.Tensor or list of torch.Tensor): In most cases, it's node tensor; Sometimes, it can be edges (node_tensor, node_tensor); 
        dst (torch.Tensor or list of torch.Tensor): In most cases, it's node tensor; Sometimes, it can be edges (node_tensor, node_tensor); 
        flag_value (int): 
        default_value (int): 

    Returns:
        torch.Tensor: Flag

    Example:
        # Case 1 : remove edges (it's used in PinSAGESampler)
        # small_graph : ([1,2,3], [1,2,3])
        # large_graph : ([1,1,2,2,3,3], [1,2,2,3,3,4])
        # We want remove all small graph's edges from large_graph

        mask = Flag_scatter(Query(samll_graph, 'coo'), Query(large_graph, 'coo'), 0, 1)
        res_g = Filter_by_flag(large_graph, mask, 'edge')
        # mask is [0,1,0,1,0,1]
        # res_g is ([1,2,3], [2,3,4])
    """
    pass

def SpMM(Graph, src_data : torch.Tensor, op : str):
    """_summary_

    Args:
        Graph (Graph): 
        src_data (torch.Tensor): 
        op (str): "sum", "max", "min"

    Returns:
        torch.Tensor: 
    """
    pass

def SDDMM(Graph, src_data : torch.Tensor, dst_data : torch.Tensor, op : str):
    """_summary_

    Args:
        Graph (Graph): 
        src_data (torch.Tensor): 
        dst_data (torch.Tensor): 
        op (str): "div", "mul", "add", "assign"

    Returns:
        torch.Tensor: 
    """
    pass




