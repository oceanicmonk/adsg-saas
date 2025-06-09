import streamlit as st
import plotly.graph_objects as go
import os
from datetime import datetime
from collections import defaultdict, deque
import math
import matplotlib.pyplot as plt
import networkx as nx

# Trial Tracking
def track_trial():
    current_month = datetime.now().strftime("%Y-%m")
    log_file = "usage.log"
    user_id = st.session_state.get("user_id", "anonymous")
    try:
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = f.readlines()
            user_key = f"{current_month}:{user_id}"
            for i, line in enumerate(logs):
                if user_key in line:
                    count = int(line.split(":")[-1].strip()) + 1
                    logs[i] = f"{user_key}:{count}\n"
                    with open(log_file, "w") as f:
                        f.writelines(logs)
                    return count
            logs.append(f"{user_key}:1\n")
            with open(log_file, "w") as f:
                f.writelines(logs)
            return 1
        else:
            with open(log_file, "w") as f:
                f.write(f"{user_key}:1\n")
            return 1
    except Exception as e:
        st.error(f"Error tracking trials: {e}")
        return 0

# Check Premium Status
def is_premium_user(user_id):
    premium_file = "premium_users.txt"
    if os.path.exists(premium_file):
        with open(premium_file, "r") as f:
            premium_users = [line.strip() for line in f]
        return user_id in premium_users
    return False

# SSC Generation
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
            current = lcm(current, 10) if isinstance(current, int) else current
        else:
            continue
        if current is None:
            return None, None
    return current, gcd_result

# SSG Class and Metrics
class SSG:
    def __init__(self, vertices, edges):
        self.V = vertices
        self.E = edges
        self.adj = defaultdict(list)
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

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
    distances = bfs(ssg, root)
    leaves = [v for v in ssg.V if len(ssg.adj[v]) == 1]
    if not leaves:
        return 0.0
    avg_dist = sum(distances[l] for l in leaves) / len(leaves)
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

number1 = st.number_input("First Number", value=7, step=1, min_value=1)
number2 = st.number_input("Second Number", value=20058, step=1, min_value=1)

trial_count = track_trial()
st.write(f"Trials this month: {trial_count}/100")

# Optional Email Prompt
user_id = st.session_state.get("user_id", "anonymous")
if trial_count > 100 and not is_premium_user(user_id):
    user_id = st.text_input("Enter Your Email for Premium Access", value=user_id)
    if user_id != "anonymous":
        st.session_state["user_id"] = user_id
    st.error("You've reached your free trial limit of 100 this month.")
    st.warning("Premium access ($5/month or ₹420/month) is available via Google Pay UPI.")
    st.write("Contact: oceanicmonk@gmail.com | UPI: oceanicmonk-1@oksbi")
    st.write("Send ₹420 (or $5) and email the transaction ID to oceanicmonk@gmail.com for premium access.")
    st.write("(Note: For international users, please contact oceanicmonk@gmail.com for alternative payment options.)")
elif st.button("Request Premium Access"):
    user_id = st.text_input("Enter Your Email for Premium Access", value=user_id)
    if user_id != "anonymous":
        st.session_state["user_id"] = user_id
    st.warning("Premium access ($5/month or ₹420/month) is available via Google Pay UPI.")
    st.write("Contact: oceanicmonk@gmail.com | UPI: oceanicmonk-1@oksbi")
    st.write("Send ₹420 (or $5) and email the transaction ID to oceanicmonk@gmail.com for premium access.")
    st.write("(Note: For international users, please contact oceanicmonk@gmail.com for alternative payment options.)")

if st.button("Generate"):
    ops = ["GCD", "LCM"]
    ssc_result, gcd_result = generate_ssc(number1, number2, ops)
    if ssc_result is not None and gcd_result is not None:
        st.write(f"SSC Result: {ssc_result}")
        vertices = list(set([number1, number2, gcd_result, ssc_result]))
        edges = []
        if number1 != gcd_result:
            edges.append((number1, gcd_result))
        if number2 != gcd_result:
            edges.append((number2, gcd_result))
        if gcd_result != ssc_result:
            edges.append((gcd_result, ssc_result))
        ssg = SSG(vertices, edges)
        beta_0, beta_1 = compute_betti_numbers(ssg)
        euler_char = compute_euler_characteristic(ssg)
        sci = compute_sci(ssg, root=gcd_result)
        gdi = compute_gdi(ssg)
        sfd = compute_sfd(ssg, root=gcd_result)
        st.write(f"Betti Numbers: β0 = {beta_0}, β1 = {beta_1}")
        st.write(f"Euler Characteristic: {euler_char}")
        st.write(f"Structural Complexity Index (SCI): {sci:.3f}")
        st.write(f"Graph Dispersion Index (GDI): {gdi:.3f}")
        st.write(f"Symbolic Fractal Dimension (SFD): {sfd:.3f}")
        G = nx.Graph()
        G.add_nodes_from(vertices)
        G.add_edges_from(edges)
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=8, edge_color='gray')
        edge_labels = {(u, v): "GCD" if v == gcd_result else "LCM" for u, v in edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        st.pyplot(plt)
        # Premium Features
        if is_premium_user(st.session_state.get("user_id", "anonymous")) or trial_count <= 100:
            st.success("Premium Access: Unlocked 3D Visualization and Report!")
            pos_3d = nx.spring_layout(G, dim=3, seed=42)
            x = [pos_3d[v][0] for v in vertices]
            y = [pos_3d[v][1] for v in vertices]
            z = [pos_3d[v][2] for v in vertices]
            fig = go.Figure(data=[
                go.Scatter3d(x=x, y=y, z=z, mode='markers+text', text=vertices,
                             marker=dict(size=12, color='blue'))
            ])
            fig.update_layout(title="3D SSG Visualization", scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
            st.plotly_chart(fig)
            report = f"ADSG Visualization Tool Report\n\nInputs: {number1}, {number2}\nSSC Result: {ssc_result}\n\nMetrics:\n- Betti Numbers: β0 = {beta_0}, β1 = {beta_1}\n- Euler Characteristic: {euler_char}\n- SCI: {sci:.3f}\n- GDI: {gdi:.3f}\n- SFD: {sfd:.3f}"
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"adsg_report_{number1}_{number2}.txt",
                mime="text/plain"
            )
        else:
            st.info("Premium features (3D Visualization and Report) require a subscription. Click 'Request Premium Access' for details.")
    else:
        st.error("Error generating SSC. Check inputs or operations.")