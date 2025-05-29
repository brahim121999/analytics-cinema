import streamlit as st

# User interface with Streamlit
st.set_page_config(
    layout="wide",
    page_title="MovieLens Data Analysis",
    page_icon="🎬"  # Unicode emoji directly
)

col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image(
        "https://raw.githubusercontent.com/brahim121999/analytics-cinema/main/streamlit_app/photo.png",
        width=80,
        use_container_width=False,
    )

with col2:
    st.markdown(
        """
        <h1 style='text-align: center; margin-bottom: 0;'>MovieLens Data Exploration</h1>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div style='text-align: right;'>
            <a href="https://www.linkedin.com/in/ibrahim-braham/" target="_blank" style='text-decoration: none; color: #0077b5;'>
                <strong>Ibrahim BRAHAM</strong>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write(" ")
st.write(" ")

st.markdown("# **Phase 1: Python Development & API Architecture**")

st.markdown(
    """
    <a href="https://github.com/brahim121999/backend-cinema" target="_blank">
        <button style="background-color: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-size: 16px;">
            📦 Click to View Phase 1 : Backend API & SDK code Code
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

st.write(" ")
st.write(" ")
st.write(" ")

st.markdown("# **Phase 2: Data Analysis - Exploration and Visualization**")

st.markdown(
    """
    <a href="https://github.com/brahim121999/analytics-cinema" target="_blank">
        <button style="background-color: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-size: 16px;">
            📊 Click to View Phase 2 : MovieLens Analysis Code
        </button>
    </a>
    """,
    unsafe_allow_html=True
)
