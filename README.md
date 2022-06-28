# Graph-centric Sampling Interfaces
Conduct transformations on bipartite graphs for subgraph sampling
* Easy to understand without deep understanding of the underlying system implementation
* Naturally support for graph-wise sampling and layer-wise sampling
* Graph samples can be directly used for the downstream tasks

## Bipartite Graph Structure
Bipartite Graph
* SrcNodes, DstNodes, Edges
  * SrcNodes and DstNodes are uniqued
  * We also use ‘AllNodes’ to represent the union of SrcNodes and DstNodes
* Store data with SrcData, DstData, EdgeData dictionaries

Transformations
* NodeFilter(NodeSetName, FilterFunc);
  * Filter nodes in NodeSetName, which can be ‘SrcNode’, ‘DstNode’ or ‘AllNode’
* EdgeFilter
* NeighborFilter(NodeSetName, FilterFunc);
  *  Filter neighbors of each node in the NodeSetName set, which can be ‘SrcNode’ or ‘DstNode’.

Properties
*  Nodes SrcNodes(Unique : bool); 
*  Nodes DstNodes(Unique : bool);
*  Nodes AllNodes();

## Common Operations
Extract a subgraph with a subset of seed nodes

* g.NodeFilter(‘DstNode’, Fn.in, seeds)

Sample in-neighborhood of a subgraph
* subg.NeighborFilter(‘DstNode’, Fn.random, fanout=25)

Biased Sampling
* Subg.NeighborFilter(‘DstNode’, Fn.random, fanout=25, bias=subg.DstData(‘w’))

Layerwise Sampling
* Subg.NodeFilter(‘SrcNode’, Fn.random, fanout=100)

Get graph properties
* g.SrcNodes()
* g.DstNodes()
