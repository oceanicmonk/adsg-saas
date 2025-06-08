import streamlit as st

st.set_page_config(page_title="Terms and Conditions", layout="wide")

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
    <h1>Terms and Conditions</h1>
    <p>Last updated: June 08, 2025</p>
    
    <h2>1. Acceptance of Terms</h2>
    <p>By accessing or using the ADSG Visualization Tool ("Service") provided by Serene Glade, you agree to be bound by these Terms and Conditions ("Terms"). If you do not agree, please do not use the Service.</p>
    
    <h2>2. Service Description</h2>
    <p>The Service generates Symbolic Shape Graphs (SSG) using GCD and LCM operations. Free users receive 50 trials/month with 2D and 3D visualizations. Premium users ($5/month ≈ ₹{st.session_state.get('inr_price', 420)}/month) receive unlimited trials and downloadable reports.</p>
    
    <h2>3. Payments</h2>
    <p>Premium subscriptions are processed via Razorpay. The subscription fee is $5/month (approximately ₹{st.session_state.get('inr_price', 420)}/month, subject to exchange rates). Refunds and cancellations are governed by our <a href="/refund_policy" target="_self">Refund and Cancellation Policy</a>.</p>
    
    <h2>4. User Responsibilities</h2>
    <p>You must provide accurate information during registration and payment. You agree not to misuse the Service or attempt to circumvent trial limits.</p>
    
    <h2>5. Privacy</h2>
    <p>Your personal information is handled in accordance with our <a href="/privacy_policy" target="_self">Privacy Policy</a>.</p>
    
    <h2>6. Limitation of Liability</h2>
    <p>To the maximum extent permitted by law, Serene Glade is not liable for any damages arising from the use or inability to use the Service.</p>
    
    <h2>7. Changes to Terms</h2>
    <p>We may update these Terms at our discretion. Continued use of the Service after changes constitutes acceptance of the updated Terms.</p>
    
    <h2>8. Contact</h2>
    <p>For questions, contact us at <a href="/contact" target="_self">oceanicmonk@gmail.com</a>.</p>
    </div>
""", unsafe_allow_html=True)