# Holistic View Path Highlighting Fix - Implementation Plan

## Problem Analysis

**Current Behavior:**
- `findUpstream()` usa condizione `neighbor_order > current_order`
- `findDownstream()` usa condizione `neighbor_order < current_order`
- Questo impedisce traversal attraverso nodi dello stesso layer

**Example:**
```
evo_niche (Application, order=3)
  ← evo_svc (Application, order=3)  [BLOCKED: same order!]
    ← proc_evolution (Business, order=4)
      ← goal_evolve (Motivation, order=5)
```

Con la logica attuale, si ferma a `evo_niche` perché `evo_svc` ha lo stesso `order`.

**Test con >= invece di >:**
- Trova 43 nodi (TROPPI!)
- Attraversa TUTTO il grafo connesso dell'Application layer
- Non è il comportamento desiderato

## Requirements (User Specification)

Quando si fa mouse-over su un nodo, evidenziare:

1. **Upstream path**: Path che collega il nodo indirettamente al Motivation Layer
2. **Downstream path**: Path che collega il nodo direttamente ai Technology Devices

Key requirements:
- Path deve attraversare layer intermedi se necessario
- Path deve essere **rilevante** (non tutto il grafo)
- Path deve mostrare la connessione architetturale logica

## Proposed Solution: Hybrid BFS Traversal

### Algorithm Design

**Upstream Traversal (toward Motivation):**
1. Start from current node
2. Use BFS (breadth-first search) to find shortest paths
3. Prioritize neighbors with higher layer order
4. Allow same-layer traversal ONLY if it leads to higher layers
5. Stop when reaching Motivation layer

**Downstream Traversal (toward Devices):**
1. Start from current node
2. Use BFS to find shortest paths
3. Prioritize neighbors with lower layer order
4. Allow same-layer traversal ONLY if it leads to lower layers
5. Stop when reaching Technology_Device nodes

### Implementation Strategy

**Option 1: Two-Phase Traversal (Recommended)**

```javascript
function findUpstreamPath(startId) {
  const queue = [{id: startId, distance: 0}];
  const visited = new Set([startId]);
  const pathNodes = new Set([startId]);
  const pathLinks = new Set();
  
  while (queue.length > 0) {
    const {id: currentId, distance} = queue.shift();
    const currentNode = nodeMap.get(currentId);
    const currentOrder = getLayerOrder(currentNode);
    
    // If reached Motivation layer, continue to explore only Motivation layer
    const reachedMotivation = currentNode.layer === 'Motivation';
    
    graphData.links.forEach(link => {
      const neighborId = getNeighborId(link, currentId);
      if (!neighborId || visited.has(neighborId)) return;
      
      const neighbor = nodeMap.get(neighborId);
      const neighborOrder = getLayerOrder(neighbor);
      
      // Traversal rules:
      // 1. Always traverse to higher layers
      // 2. Traverse same layer only if distance is small (< 2)
      // 3. Never traverse to lower layers in upstream search
      const shouldTraverse = 
        (neighborOrder > currentOrder) ||  // Higher layer: always
        (neighborOrder === currentOrder && distance < 2 && !reachedMotivation);  // Same layer: limited
      
      if (shouldTraverse) {
        visited.add(neighborId);
        pathNodes.add(neighborId);
        pathLinks.add(link);
        queue.push({id: neighborId, distance: distance + 1});
      }
    });
  }
  
  return {nodes: pathNodes, links: pathLinks};
}
```

**Option 2: Directional Priority Search**

```javascript
function findUpstreamPath(startId) {
  const pathNodes = new Set();
  const pathLinks = new Set();
  
  // Recursive DFS with direction priority
  function traverse(nodeId, visitedInPath) {
    if (visitedInPath.has(nodeId)) return;
    
    pathNodes.add(nodeId);
    visitedInPath.add(nodeId);
    
    const currentNode = nodeMap.get(nodeId);
    const currentOrder = getLayerOrder(currentNode);
    
    // Find all neighbors
    const neighbors = graphData.links
      .filter(link => 
        (link.source.id || link.source) === nodeId || 
        (link.target.id || link.target) === nodeId
      )
      .map(link => {
        const neighborId = getNeighborId(link, nodeId);
        const neighbor = nodeMap.get(neighborId);
        return {
          id: neighborId,
          order: getLayerOrder(neighbor),
          link: link,
          neighbor: neighbor
        };
      })
      .filter(n => !visitedInPath.has(n.id));
    
    // Sort by priority: higher layers first
    neighbors.sort((a, b) => b.order - a.order);
    
    // Traverse higher layers first, then same layer
    for (const n of neighbors) {
      if (n.order >= currentOrder) {  // Allow same layer
        pathLinks.add(n.link);
        traverse(n.id, new Set(visitedInPath));
      }
    }
  }
  
  traverse(startId, new Set());
  return {nodes: pathNodes, links: pathLinks};
}
```

**Option 3: Shortest Path Only (Dijkstra-like)**

Use Dijkstra's algorithm to find THE shortest path to any Motivation node, not all possible paths.

```javascript
function findShortestPathToMotivation(startId) {
  const distances = new Map();
  const previous = new Map();
  const unvisited = new Set(graphData.nodes.map(n => n.id));
  
  distances.set(startId, 0);
  
  while (unvisited.size > 0) {
    // Find node with minimum distance
    let current = null;
    let minDist = Infinity;
    for (const nodeId of unvisited) {
      const dist = distances.get(nodeId) ?? Infinity;
      if (dist < minDist) {
        minDist = dist;
        current = nodeId;
      }
    }
    
    if (!current || minDist === Infinity) break;
    
    const currentNode = nodeMap.get(current);
    
    // If reached Motivation, reconstruct path
    if (currentNode.layer === 'Motivation') {
      return reconstructPath(previous, current);
    }
    
    unvisited.delete(current);
    const currentOrder = getLayerOrder(currentNode);
    
    // Update neighbors
    graphData.links.forEach(link => {
      const neighborId = getNeighborId(link, current);
      if (!neighborId || !unvisited.has(neighborId)) return;
      
      const neighbor = nodeMap.get(neighborId);
      const neighborOrder = getLayerOrder(neighbor);
      
      // Only consider upward or same-level moves
      if (neighborOrder >= currentOrder) {
        const alt = minDist + 1;
        if (alt < (distances.get(neighborId) ?? Infinity)) {
          distances.set(neighborId, alt);
          previous.set(neighborId, {from: current, link: link});
        }
      }
    });
  }
  
  return {nodes: new Set(), links: new Set()};  // No path found
}
```

## Recommended Approach

**Option 1 (Two-Phase Traversal)** is recommended because:

1. ✅ **Controlled exploration**: Limits same-layer traversal with distance parameter
2. ✅ **Finds relevant paths**: Doesn't explore entire graph
3. ✅ **Flexible**: Can tune `distance` limit for different behaviors
4. ✅ **BFS-based**: Naturally finds shorter paths first
5. ✅ **Readable**: Easy to understand and debug

## Implementation Steps

### Step 1: Refactor findUpstream/findDownstream

Replace recursive DFS with BFS-based traversal:

```javascript
function highlightConnected(nodeId) {
  const nodeMap = new Map(graphData.nodes.map(n => [n.id, n]));
  
  const upstreamResult = findUpstreamPathBFS(nodeId, nodeMap);
  const downstreamResult = findDownstreamPathBFS(nodeId, nodeMap);
  
  const highlightedNodes = new Set([
    ...upstreamResult.nodes,
    ...downstreamResult.nodes
  ]);
  
  const highlightedLinks = new Set([
    ...upstreamResult.links,
    ...downstreamResult.links
  ]);
  
  // Apply highlighting
  nodeElements.classed('dimmed', d => !highlightedNodes.has(d.id));
  nodeElements.classed('highlight', d => d.id === nodeId);
  linkElements.classed('dimmed', d => !highlightedLinks.has(d));
  linkElements.classed('highlight', d => highlightedLinks.has(d));
}
```

### Step 2: Implement BFS Traversal Functions

```javascript
function findUpstreamPathBFS(startId, nodeMap) {
  const MAX_SAME_LAYER_DISTANCE = 2;  // Tunable parameter
  
  const queue = [{id: startId, distance: 0}];
  const visited = new Set([startId]);
  const pathNodes = new Set([startId]);
  const pathLinks = new Set();
  
  while (queue.length > 0) {
    const {id: currentId, distance} = queue.shift();
    const currentNode = nodeMap.get(currentId);
    if (!currentNode) continue;
    
    const currentOrder = getLayerOrder(currentNode);
    const reachedMotivation = currentNode.layer === 'Motivation';
    
    graphData.links.forEach(link => {
      const srcId = link.source.id || link.source;
      const tgtId = link.target.id || link.target;
      const neighborId = (srcId === currentId) ? tgtId : 
                         (tgtId === currentId) ? srcId : null;
      
      if (!neighborId || visited.has(neighborId)) return;
      
      const neighbor = nodeMap.get(neighborId);
      if (!neighbor) return;
      
      const neighborOrder = getLayerOrder(neighbor);
      
      // Traversal logic
      const isHigherLayer = neighborOrder > currentOrder;
      const isSameLayer = neighborOrder === currentOrder;
      const withinSameLayerLimit = distance < MAX_SAME_LAYER_DISTANCE;
      
      const shouldTraverse = 
        isHigherLayer ||  // Always traverse to higher layers
        (isSameLayer && withinSameLayerLimit && !reachedMotivation);
      
      if (shouldTraverse) {
        visited.add(neighborId);
        pathNodes.add(neighborId);
        pathLinks.add(link);
        queue.push({
          id: neighborId,
          distance: isSameLayer ? distance + 1 : 0  // Reset distance on layer change
        });
      }
    });
  }
  
  return {nodes: pathNodes, links: pathLinks};
}

function findDownstreamPathBFS(startId, nodeMap) {
  // Mirror logic for downstream (toward devices)
  // Same structure but with neighborOrder < currentOrder for lower layers
}
```

### Step 3: Testing

Test cases:
1. `evo_niche` → Should reach Motivation layer via `evo_svc → proc_evolution → goal_*`
2. `evo_niche` → Should reach Device layer via `evo_svc → hw_android/linux/mimx`
3. Any Motivation node → Should highlight downstream to all connected devices
4. Any Device node → Should highlight upstream to connected Motivation goals

### Step 4: Tuning Parameters

Adjust `MAX_SAME_LAYER_DISTANCE` based on visual feedback:
- `1`: Very strict, only immediate same-layer neighbors
- `2`: Moderate (recommended), allows small clusters
- `3+`: More permissive, larger exploration

## Alternative: Simplest Fix

If the above is too complex, the **simplest fix** is:

```javascript
// In findUpstream:
if (neighbor && getLayerOrder(neighbor) >= getLayerOrder(currentNode)) {
  // BUT: add max depth limit to prevent exploring entire layer
  if (depth < 3) {  // Max 3 hops in same layer
    // ... traverse
  }
}
```

This requires adding a `depth` parameter to the recursive function.

## Validation Criteria

After implementation, verify:

- [ ] `evo_niche` hover shows path to Motivation layer
- [ ] `evo_niche` hover shows path to Device layer
- [ ] No performance degradation (< 100ms per hover)
- [ ] Visually intuitive highlighting
- [ ] No excessive node highlighting (max ~20 nodes per hover)

## Files to Modify

- `docs/holistic_view.html` (lines 751-814: `highlightConnected` function)

## Rollback Plan

If new implementation causes issues:
1. Revert to original logic
2. Add a console warning: "Limited path highlighting due to same-layer connections"
3. Document as known limitation

---

**Recommendation**: Implement Option 1 (Two-Phase BFS Traversal) with `MAX_SAME_LAYER_DISTANCE = 2`
