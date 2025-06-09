import streamlit as st

st.set_page_config(page_title="Contact", layout="wide")

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
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="content">
    <h1>Contact Us</h1>
    <p>For any questions or support regarding the ADSG Visualization Tool, please reach out to us:</p>
    <p><strong>Email</strong>: <a href="mailto:oceanicmonk@gmail.com">oceanicmonk@gmail.com</a></p>
    <p><strong>Phone</strong>: <a href="tel:+919745059169">+91 9745059169</a></p>
    <p><strong>Address</strong>: Ambalaparambil, Kerala-676509, India</p>
    <p><strong>Business Name</strong>: Serene Glade</p>
    </div>
""", unsafe_allow_html=True)
