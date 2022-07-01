# Graph-centric Interfaces

Conduct transformations on **bipartite graphs** for subgraph sampling.

Graph transformations : **bipartite graph -> bipartite graph**

* **Easy to understand without deep understanding of the underlying system implementation**
* **Naturally support for node-wise, layer-wise sampling and graph-wise sampling**
* **Graph sampled can be directly used for the downstream tasks**

## Structures

**Bipartite Graph**

Each graph is a bipartite graph;

Each g has **SrcNodes**, **DstNodes**, **Edges**;

Store data with **NodeData**, **EdgeData** dictionaries. For heterogeneous graph, we use **SrcNodeData** and **DstNodeData** instead of **NodeData**;

* **Transformations** (Bipartite Graph -> Bipartite Graph)

  * **NodeFilter(NodeSetName, FilterFunc)**
    * Filter nodes in NodeSetName, which can be `SrcNode`, `DstNode` or `AllNode`
  * **EdgeFilter(FilterFunc)**
    * Filter edges by function return value [bool]
  * **NeighborFilter(NodeSetName, FilterFunc)**
    * Filter neighbors of each node in the NodeSetName set, which can be `SrcNode` or `DstNode`

* **Properties** (Bipartite Graph -> Nodes or (Nodes, Nodes))

  * Nodes SrcNodes(Unique : bool);
  * Nodes DstNodes(Unique : bool)
  * Nodes AllNodes()
    * For heterogeneous graph, it will raise an error. [Undefined]
  
  * Tuple(Nodes, Nodes) Edges()
    * Return (g.SrcNodes(False), g.DstNodes(False))
  
  ```python
  # case study for Bipartite Graph Properties
  
  g = CreateGraph('coo', [[1,1,3], [1,4,4]], FirstIsSrc=True)
  # g.SrcNodes(unique=True) = [1,3]
  # g.SrcNodes(unique=False) = [1,1,3]
  # g.DstNodes(unique=True) = [1,4]
  # g.DstNodes(uniuqe=False) = [1,4,4]
  # g.AllNodes() = [1,4,3]
  # g.Edges() = ([1,1,3], [1,4,4])
  ```

* Other methods
  * g.num_nodes()
  * g.num_edges()
  * g.degrees(NodeSetName)
    * NodeSetName is SrcNode or DstNode or AllNodes
    * AllNodes for heterogeneous graph is undefined
  
**Set**
  
**Append writes only**. It should be only used in **Graph Transformations**.
  
Method
  
  * Void insert(Nodes node)
  * Nodes iterate()
  
  ```python
  # case study for Set
  ret = Set()
  ret.insert([1,2,1]) # ret = [1,2]
  ret.insert([4,2,3]) # ret = [1,2,4,3]
  # ret.iterate() = [1,2,4,3]
  ```
  
**HashTable**
  
All keys have the same type and all values have the same type.
  
Method:
  
  * Void update(key, value, op)
    * op is in ['add', 'assign', 'min', 'max']
  * Void delete(key)
  * Tuple(Keys, Values) iterate()
  
  ```python
  # case study for HashTable
  Dir = HashTable()
  Dir.update([1,2,3], [4,5,4], op='add') 
  # key = [1,2,3], value = [4,5,4]; for key not in HashTable, we just do 'assign'
  Dir.update([1,2,3], [1,2,3], op='add') 
  # key = [1,2,3], value = [5,7,7]
  Dir.update([1,1,1], [5,4,2], op='min') 
  # key = [1,2,3], value = [2,7,7]
  Dir.delete([2,3]) 
  # key = [1], value = [2]
  # Dir.iterate() = ([1], [2])
  ```
  
## Transformations

### NodeFilter(NodeSetName, FilterFunc)

* Filter nodes in NodeSetName, which can be `SrcNode`, `DstNode` or `AllNode`

* FilterFunc is a built in function, which can be Fn.in(), Fn.notin(), Fn.random()

  ```python
  Fn.in(Nodes node_set) 
  # it NodeSetName[i] is in node_set, ret[i] will be True, otherwise False.
  Fn.notin(Nodes node_set)
  # The opposite effect of Fn.in
  Fn.random(num_pick, bias=None, replace=False)
  # Do random sampling on NodeSetName
  Fn.flagged(Bool[] mask)
  # Filter NodeSetName[i] according to mask[i]
  ```

### EdgeFilter(FilterFunc)

* Filter edges by function return value [bool].

* FilterFunc is a function that returns Bool[], and the return value should be the same length as g.num_edges().

* Users can define their own functions.

* We also provide some built in functions: Fn.Edge.in, Fn.Edge.notin, Fn.Edge.flagged.

  ```python
  Fn.Edge.in(Source, Target)
  # if Source[i] is in Target, ret[i] will be True, otherwise it will be False.
  ## Case 1
  ## Fn.Edge.in([1,2,3,4], [2,4,6]), it will return [F, T, F, T]
  ## Case 2
  ## Fn.Edge.in(([1,2,4,4], [1,2,2,4]), ([2,4], [2,4])), it will return [F, T, F, T]
  ## (1,1) is not in Target, (2, 2) is in Target, (4, 2) is not in Target, (4, 4) is in Target.
  
  Fn.Edge.notin(Source, Target)
  # The opposite effect of Fn.Edge.in
  
  Fn.Edge.flagged(Bool[] mask) 
  # len(mask) should be equal to g.num_edges(). 
  # If mask[i] is True, edge[i] will be kept, otherwise edge[i] will be deleted.
  
  # Case
  ## use built in function
  g.EdgeFilter(Fn.Edge.notin(g.EdgeData['eids'], reverse_ids)
  ## use udf function
  udf = lambda src, dst, T : T[src] < T[dst]
  T = g.NodeData['T']
  g.EdgeFilter(udf(g.SrcNodes(uniuqe=False), g.DstNodes(uniuqe=False), T))
  ```

### NeighborFilter(NodeSetName, FilterFunc)

* Filter neighbors of each node in the NodeSetName set, which can be `SrcNode` or `DstNode`

* FilterFunc is a built in funciton, which can be Fn.random, Fn.unique

  ```python
  Fn.random(num_picks, bias=None, replace=False, keep_dim=False) 
  # to sample the neighbors of NodeSetName
  # If keep_dim = True, it will keep the shape of g and replace the invalid node with -1
  ## Case
  g = CreateGraph('coo', [[1,1,1,1], [1,2,3,4]])
  subg = g.NeighFilter('SrcNode', Fn.random(2, keep_dim=True))
  ## subg is [[1,1,1,1], [1,2,-1,-1]
  subg = g.NeighFilter('SrcNode', Fn.random(2, keep_dim=False))
  ## subg is [[1,1], [1,2]]
  
  Fn.unique(keep_dim=False) 
  # to dedup the neighbors of NodeSetName. Try to creata a simple graph of NodeSetName.
  ```

## Other Functions

* CreateGraph

  ```python
  CreateGraph(format : str, Tensor[], FirstIsSrc=True, heterGraph=False) -> Graph
  # format is in ['coo', 'csr', 'csc']
  ```

* SpMM

  ```python
  SpMM(NodeSetName, root_data : Tensor, neigh_data : Tensor, udf) -> Tensor
  # has the same semantics as SpMM in DGL, but only for scalars. root_data, neigh_data are 1-D.
  ```

* SDDMM

  ```python
  SDDMM(NodeSetName, root_data : Tesnor, neigh_data : Tensor, edge_data : Tensor, udf) -> Tensor
  # has the same semantics as SDDMM in DGL, but only for scalars. root_data, neigh_data, edge_data are 1-D.
  ```
  
* Any operations supported by `PyTorch`.

## Common Opeartions

```python
# Extract a subgraph with a subset of seed nodes
# Return a subgrah which contains only the seeds and their neighbors.
g.NodeFilter('DstNode', Fn.in(seeds))
# Sample in-neighborhood of a subgraph
subg.NeighborFilter('DstNode', Fn.random(fanout))
# Biased Sampling
Subg.NeighborFilter('DstNode', Fn.random(25, bias=subg.DstData('w'))
# Layerwise Sampling
Subg.NodeFilter('SrcNode', Fn.random(fanout))
# in_subgraph
Subg.NodeFilter('AllNode', Fn.in(nodes))                  
# Remove edges
## Case 1
g.EdgeFilter(Fn.Edge.notin(g.EdgeData['eid'], reverse_ids))
## Case 2
g.EdgeFilter(Fn.Edge.notin(g.Edges(), neg.Edges()))                    
## Case 3
Udf = lambda src, dst, T : T[src] > T[dst]
g.EdgeFilter(Udf(g.SrcNodes(unique=False), g.DstNodes(unique=False), g.NodeData['T'])
# Get graph properties
g.SrcNodes(unique=False)
g.DstNodes(unique=True)
g.Edges()
```

##  Known Issues

* **SEAL** could not be expressed efficiently
