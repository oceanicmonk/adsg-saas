import streamlit as st

st.set_page_config(page_title="Privacy Policy", layout="wide")

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

st.markdown("""
    <div class="content">
    <h1>Privacy Policy</h1>
    <p>Last updated: June 08, 2025</p>
    
    <h2>1. Introduction</h2>
    <p>Serene Glade ("we," "us," or "our") operates the ADSG Visualization Tool ("Service"). This Privacy Policy explains how we collect, use, store, and protect your personal information.</p>
    
    <h2>2. Information We Collect</h2>
    <p>We collect:
    - <strong>Personal Information</strong>: Email address provided during payment or registration.
    - <strong>Payment Information</strong>: Processed securely via Razorpay, including card details and transaction data.
    - <strong>Usage Data</strong>: Trial counts and interactions with the Service, stored in usage.log.</p>
    
    <h2>3. How We Use Your Information</h2>
    <p>We use your information to:
    - Provide and improve the Service.
    - Process payments via Razorpay.
    - Communicate updates or support responses.
    - Monitor trial limits and prevent abuse.</p>
    
    <h2>4. Sharing Your Information</h2>
    <p>We share your information with:
    - Razorpay, for payment processing (subject to their <a href="https://razorpay.com/privacy/" target="_blank">Privacy Policy</a>).
    - Legal authorities, if required by law.
    We do not sell or share your data with other third parties.</p>
    
    <h2>5. Data Security</h2>
    <p>We use industry-standard measures to protect your data, but no system is completely secure. You use the Service at your own risk.</p>
    
    <h2>6. Data Retention</h2>
    <p>We retain personal information as long as your account is active or as needed to comply with legal obligations. Usage data is retained for up to 24 months.</p>
    
    <h2>7. Your Rights</h2>
    <p>You may request access, correction, or deletion of your personal information by contacting us at oceanicmonk@gmail.com. Note that some data may be required for the Service to function.</p>
    
    <h2>8. Changes to This Policy</h2>
    <p>We may update this Privacy Policy. Changes will be posted here, and continued use of the Service constitutes acceptance.</p>
    
    <h2>9. Contact</h2>
    <p>For questions, contact us at <a href="/contact" target="_self">oceanicmonk@gmail.com</a>.</p>
    </div>
""", unsafe_allow_html=True)