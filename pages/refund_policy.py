import streamlit as st

st.set_page_config(page_title="Refund and Cancellation Policy", layout="wide")

st.markdown("""
    <style>
    .content {
        font-size: 1rem; /* 14pt */
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    h1 {
        font-size: 1.25rem; /* 18pt */
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    h2 {
        font-size: 1.125rem; /* 16pt */
        color: #333;
        margin-top: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="content">
    <h1>Refund and Cancellation Policy</h1>
    <p>Last updated: June 08, 2025</p>
    
    <h2>1. Overview</h2>
    <p>Serene Glade ("we," "us," or "our") operates the ADSG Visualization Tool ("Service"). This Refund and Cancellation Policy outlines the terms for refunds and cancellations of Premium subscriptions.</p>
    
    <h2>2. Subscription Details</h2>
    <p>The Premium subscription costs $5/month (approximately ₹{st.session_state.get('inr_price', 420)}/month, subject to exchange rates) and provides unlimited trials and downloadable reports.</p>
    
    <h2>3. Refund Policy</h2>
    <p>All Premium subscription payments are non-refundable, except as required by applicable law. If you believe a payment was made in error, contact us within 7 days of the transaction at <a href="/contact" target="_self">oceanicmonk@gmail.com</a>.</p>
    
    <h2>4. Cancellation Policy</h2>
    <p>You may cancel your Premium subscription at any time by contacting us at <a href="/contact" target="_self">oceanicmonk@gmail.com</a>. Upon cancellation, you will retain Premium access until the end of the current billing cycle. No further charges will be applied.</p>
    
    <h2>5. Contact</h2>
    <p>For refund or cancellation requests, contact us at <a href="/contact" target="_self">oceanicmonk@gmail.com</a>.</p>
    </div>
""", unsafe_allow_html=True)