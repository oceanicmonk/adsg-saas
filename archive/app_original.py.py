import streamlit as st
from collections import defaultdict, deque
import math
import matplotlib.pyplot as plt
import networkx as nx

# SSC Generation (Simplified from Appendix C)
def gcd(a: int, b: int) -> int:
    return abs(a) if b == 0 else gcd(b, a % b)

def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)

def generate_ssc(x: int, y: int, ops: list) -> tuple:
    current = (x, y)
    gcd_result = None
    for op in ops:
        if op == "GCD":
            gcd_result = gcd(current[0], current[1]) if isinstance(current, tuple) else current
            current = gcd_result
        elif op == "LCM":
            current = lcm(current, 10) if isinstance(current, int) else current  # Default constant 10
        else:
            current = None  # Simplified error handling
        if current is None:
            return None, None
    return current, gcd_result

# SSG Class and Metrics from Appendix D
class SSG:
    def __init__(self, vertices, edges):
        self.V = vertices
        self.E = edges
        self.adj = defaultdict(list)
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

# BFS function in global scope
def bfs(ssg, start):
    dist = {v: float('inf') for v in ssg.V}
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in ssg.adj[u]:
            if dist[v] == float('inf'):
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

def compute_betti_numbers(ssg):
    def dfs(v, visited, component):
        visited.add(v)
        component.append(v)
        for u in ssg.adj[v]:
            if u not in visited:
                dfs(u, visited, component)
    
    visited = set()
    components = []
    for v in ssg.V:
        if v not in visited:
            component = []
            dfs(v, visited, component)
            components.append(component)
    
    beta_0 = len(components)
    beta_1 = len(ssg.E) - len(ssg.V) + beta_0
    return beta_0, beta_1

def compute_euler_characteristic(ssg):
    beta_0, beta_1 = compute_betti_numbers(ssg)
    return beta_0 - beta_1

def compute_sci(ssg, root):
    # Compute distances from root
    distances = bfs(ssg, root)
    # Identify leaves (nodes with degree 1)
    leaves = [v for v in ssg.V if len(ssg.adj[v]) == 1]
    if not leaves:
        return 0.0  # Handle edge case (e.g., no leaves)
    avg_dist = sum(distances[l] for l in leaves) / len(leaves)
    
    # Compute diameter (max distance between any two nodes)
    max_dist = 0
    for v in ssg.V:
        dist = bfs(ssg, v)
        max_d = max((d for d in dist.values() if d != float('inf')), default=0)
        max_dist = max(max_dist, max_d)
    
    return avg_dist / max_dist if max_dist > 0 else 0

def compute_gdi(ssg):
    degrees = [len(ssg.adj[v]) for v in ssg.V]
    mean_deg = 2 * len(ssg.E) / len(ssg.V) if len(ssg.V) > 0 else 0
    variance = sum((d - mean_deg) ** 2 for d in degrees) / len(ssg.V) if len(ssg.V) > 0 else 0
    std_dev = math.sqrt(variance)
    return std_dev / mean_deg if mean_deg > 0 else 0

def compute_sfd(ssg, root):
    def bfs_radius(r):
        dist = {v: float('inf') for v in ssg.V}
        dist[root] = 0
        queue = deque([root])
        nodes = set()
        while queue:
            u = queue.popleft()
            if dist[u] <= r:
                nodes.add(u)
            for v in ssg.adj[u]:
                if dist[v] == float('inf'):
                    dist[v] = dist[u] + 1
                    queue.append(v)
        return len(nodes)
    
    max_r = max(bfs(ssg, root).values(), default=0)
    if max_r == 0:
        return 0
    r = max_r
    vr = bfs_radius(r)
    vr2 = bfs_radius(r / 2)
    return math.log(vr / vr2) / math.log(2) if vr2 > 0 else 0

# Streamlit Interface
st.title("ADSG Visualization Tool")

number1 = st.number_input("First Number", value=7, step=1)
number2 = st.number_input("Second Number", value=6000000, step=1)

if st.button("Generate"):
    # Generate SSC with operations [GCD, LCM] as per example in C.1.3
    ops = ["GCD", "LCM"]
    ssc_result, gcd_result = generate_ssc(number1, number2, ops)
    
    if ssc_result is not None and gcd_result is not None:
        st.write(f"SSC Result: {ssc_result}")
        
        # Dynamically construct SSG based on SSC computation
        vertices = [number1, number2, gcd_result, ssc_result]
        edges = [(number1, gcd_result), (number2, gcd_result), (gcd_result, ssc_result)]
        ssg = SSG(vertices, edges)
        
        # Compute metrics
        beta_0, beta_1 = compute_betti_numbers(ssg)
        euler_char = compute_euler_characteristic(ssg)
        sci = compute_sci(ssg, root=gcd_result)
        gdi = compute_gdi(ssg)
        sfd = compute_sfd(ssg, root=gcd_result)
        
        # Display results
        st.write(f"Betti Numbers: β0 = {beta_0}, β1 = {beta_1}")
        st.write(f"Euler Characteristic: {euler_char}")
        st.write(f"Structural Complexity Index (SCI): {sci:.3f}")
        st.write(f"Graph Dispersion Index (GDI): {gdi:.3f}")
        st.write(f"Symbolic Fractal Dimension (SFD): {sfd:.3f}")
        
        # SSG Visualization with networkx and matplotlib
        G = nx.Graph()
        G.add_nodes_from(vertices)
        G.add_edges_from(edges)
        plt.figure(figsize=(8, 6))
        nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_size=8, edge_color='gray')
        st.pyplot(plt)
    else:
        st.error("Error generating SSC. Check inputs or operations.")