import streamlit as st
import plotly.graph_objects as go
import os
from datetime import datetime
from collections import defaultdict, deque
import math
import matplotlib
matplotlib.use('Agg')  # Force non-interactive backend
import matplotlib.pyplot as plt
import networkx as nx
import razorpay

# Set page configuration
st.set_page_config(page_title="ADSG Visualization Tool", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for vibrant buttons and shortened number input bars
st.markdown("""
    <style>
    /* Generate button: Vibrant lime green */
    div.stButton > button[kind="primary"] {
        background-color: #00ff7f;
        color: black;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #00e66b;
    }
    /* Upgrade to Premium button: Vibrant royal blue */
    div.stButton > button[kind="secondary"] {
        background-color: #1e90ff;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #1a7de6;
    }
    /* Other buttons (Download Report): Gray */
    div.stButton > button:not([kind="primary"]):not([kind="secondary"]) {
        background-color: #6c757d;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    div.stButton > button:not([kind="primary"]):not([kind="secondary"]):hover {
        background-color: #5a6268;
    }
    /* Shorten number input bars */
    .stNumberInput input {
        width: 15rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Trial Tracking
def track_trial():
    current_month = datetime.now().strftime("%Y-%m")
    log_file = "usage.log"
    user_id = st.session_state.get("user_email", st.session_state.get("razorpay_payment_id", "anonymous"))
    try:
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = f.readlines()
            user_key = f"{current_month}:{user_id}"
            # Clean old logs (optional: remove entries from previous months)
            logs = [line for line in logs if current_month in line]
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
st.title("ADSG Visualization Tool 📈")
st.markdown("""
    **Welcome to the ADSG Visualization Tool!**  
    This application generates Symbolic Shape Graphs (SSG) from two numbers using GCD and LCM operations.  
    - Free users get 50 trials/month with 2D and 3D visualizations.  
    - Premium users ($5/month or ₹420/month) get unlimited trials with 3D visualizations and reports.  
    Try it now with the inputs below!
""", unsafe_allow_html=True)

# Input fields
number1 = st.number_input("First Number", value=7, min_value=1, step=1)
number2 = st.number_input("Second Number", value=20058, min_value=1, step=1)

# Trial tracking
trial_count = track_trial()
st.session_state["trial_count"] = trial_count
st.write(f"Trials this month: {trial_count}/50")

# Initialize session state
if "results" not in st.session_state:
    st.session_state["results"] = None

# Razorpay Integration
if "razorpay_client" not in st.session_state:
    key_id = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_123456789")
    key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "rzp_test_abcdef123456")
    st.session_state["razorpay_client"] = razorpay.Client(auth=(key_id, key_secret))

# Payment form
with st.form(key="payment_form"):
    st.info("Unlock Unlimited Trials & Reports for Just $5/₹420 Monthly!")
    st.markdown("**Want unlimited access?** Upgrade to Premium ($5/month or ₹420/month) for unlimited trials and enhanced features!", unsafe_allow_html=True)
    user_email = st.text_input("Enter Your Email for Premium Access", value=st.session_state.get("user_email", ""), key="email_input")
    submitted = st.form_submit_button("Upgrade to Premium ($5/month or ₹420/month)", type="secondary")

if submitted:
    if not user_email:
        st.error("Please enter a valid email to proceed with payment.")
    else:
        try:
            order = st.session_state["razorpay_client"].order.create({
                "amount": 42000,  # ₹420 in paise
                "currency": "INR",
                "receipt": f"adsg_{trial_count}_{user_email}",
                "payment_capture": 1
            })
            st.session_state["order_id"] = order["id"]
            st.components.v1.html(f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                <script>
                var options = {{
                    "key": "{key_id}",
                    "amount": "42000",
                    "currency": "INR",
                    "name": "ADSG Visualization Tool",
                    "description": "Premium Subscription",
                    "order_id": "{order['id']}",
                    "handler": function (response) {{
                        window.location.href = window.location.href + "?payment_id=" + response.razorpay_payment_id;
                    }},
                    "prefill": {{"name": "User", "email": "{user_email}", "contact": "9999999999"}},
                    "theme": {{"color": "#4CAF50"}}
                }};
                var rzp = new Razorpay(options);
                rzp.open();
                </script>
                <p>Redirecting after payment...</p>
            """, height=400)
            st.session_state["user_email"] = user_email
        except Exception as e:
            st.error(f"Payment setup pending Razorpay key activation. Try again later or contact support. Error: {e}")

# Check trial limit before generation
if trial_count > 50 and not st.session_state.get("razorpay_payment_id"):
    st.error("You've reached your free trial limit of 50 this month. Upgrade to Premium to continue.")
else:
    # SSC Generation and Visualization
    if st.button("Generate", key="generate_button", type="primary"):
        ops = ["GCD", "LCM"]
        ssc_result, gcd_result = generate_ssc(number1, number2, ops)
        if ssc_result is not None and gcd_result is not None:
            results = {
                "ssc_result": ssc_result,
                "gcd_result": gcd_result,
                "vertices": list(set([number1, number2, gcd_result, ssc_result])),
                "edges": []
            }
            if number1 != gcd_result:
                results["edges"].append((number1, gcd_result))
            if number2 != gcd_result:
                results["edges"].append((number2, gcd_result))
            if gcd_result != ssc_result:
                results["edges"].append((gcd_result, ssc_result))
            ssg = SSG(results["vertices"], results["edges"])
            beta_0, beta_1 = compute_betti_numbers(ssg)
            euler_char = compute_euler_characteristic(ssg)
            sci = compute_sci(ssg, root=gcd_result)
            gdi = compute_gdi(ssg)
            sfd = compute_sfd(ssg, root=gcd_result)
            results.update({
                "beta_0": beta_0, "beta_1": beta_1, "euler_char": euler_char,
                "sci": sci, "gdi": gdi, "sfd": sfd
            })
            st.session_state["results"] = results
        else:
            st.error("Error generating SSC. Check inputs or operations.")

    # Display results if available
    if st.session_state.get("results"):
        results = st.session_state["results"]
        st.markdown(f"**SSC Result**: {results['ssc_result']}")
        st.markdown(f"**Betti Numbers**: β0 = {results['beta_0']}, β1 = {results['beta_1']}")
        st.markdown(f"**Euler Characteristic**: {results['euler_char']}")
        st.markdown(f"**Structural Complexity Index (SCI)**: {results['sci']:.3f}")
        st.markdown(f"**Graph Dispersion Index (GDI)**: {results['gdi']:.3f}")
        st.markdown(f"**Symbolic Fractal Dimension (SFD)**: {results['sfd']:.3f}")
        # 2D Visualization
        st.markdown("<h3 style='color: #4CAF50;'>2D Visualization</h3>", unsafe_allow_html=True)
        G = nx.Graph()
        G.add_nodes_from(results["vertices"])
        G.add_edges_from(results["edges"])
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='#90CAF9', node_size=500, font_size=8, edge_color='gray')
        edge_labels = {(u, v): "GCD" if v == results["gcd_result"] else "LCM" for u, v in results["edges"]}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        st.pyplot(plt)
        plt.close()  # Close figure to prevent memory leak
        # 3D Visualization (available for trial_count <= 50 or premium)
        if trial_count <= 50 or st.session_state.get("razorpay_payment_id"):
            st.success("Enhanced Access: 3D Visualization and Report available!")
            st.markdown("<h3 style='color: #4CAF50;'>3D Visualization</h3>", unsafe_allow_html=True)
            pos_3d = nx.spring_layout(G, dim=3, seed=42)
            x = [pos_3d[v][0] for v in results["vertices"]]
            y = [pos_3d[v][1] for v in results["vertices"]]
            z = [pos_3d[v][2] for v in results["vertices"]]
            fig = go.Figure(data=[
                go.Scatter3d(x=x, y=y, z=z, mode='markers+text', text=results["vertices"],
                             marker=dict(size=12, color='#2196F3', opacity=0.8))
            ])
            fig.update_layout(
                title="3D SSG Visualization",
                scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=800, height=600
            )
            st.plotly_chart(fig, use_container_width=True)
            if trial_count <= 50 and not st.session_state.get("razorpay_payment_id"):
                st.info("Love 3D visualizations? Upgrade to Premium for unlimited trials and downloadable reports!")
            st.markdown("<h3 style='color: #4CAF50;'>Download Report</h3>", unsafe_allow_html=True)
            report = (f"ADSG Visualization Tool Report\n\nInputs: {number1}, {number2}\n"
                      f"SSC Result: {results['ssc_result']}\n\nMetrics:\n"
                      f"- Betti Numbers: β0 = {results['beta_0']}, β1 = {results['beta_1']}\n"
                      f"- Euler Characteristic: {results['euler_char']}\n"
                      f"- SCI: {results['sci']:.3f}\n- GDI: {results['gdi']:.3f}\n- SFD: {results['sfd']:.3f}")
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"adsg_report_{number1}_{number2}.txt",
                mime="text/plain",
                key="download_button"
            )
        else:
            st.info("3D Visualization and Report require a premium subscription after 50 trials. Click 'Upgrade to Premium' to proceed.")

# Handle payment success
if st.query_params.get("payment_id"):
    payment_id = st.query_params["payment_id"][0]
    st.session_state["razorpay_payment_id"] = payment_id
    st.session_state["user_email"] = st.session_state.get("user_email", "anonymous")
    # Reset trial count
    current_month = datetime.now().strftime("%Y-%m")
    log_file = "usage.log"
    user_key = f"{current_month}:{st.session_state.get('user_email', payment_id)}"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()
        with open(log_file, "w") as f:
            for line in lines:
                if user_key in line:
                    f.write(f"{user_key}:0\n")
                else:
                    f.write(line)
    st.session_state["trial_count"] = 0
    st.success(f"Payment successful! Premium access unlocked with Payment ID: {payment_id}")