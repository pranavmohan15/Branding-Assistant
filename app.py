import streamlit as st
import openai
import os
import base64
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="AI Branding Studio",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------
# UI CSS
# -------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    background: radial-gradient(circle at top,#1e293b,#020617);
    color: white;
}

/* Glass cards */

.glass-card {
    backdrop-filter: blur(18px);
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 28px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 25px;
}

/* Buttons */

.stButton>button {
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
    transition: all 0.25s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 8px 20px rgba(99,102,241,0.45);
}

/* Input styling */

div[data-baseweb="input"] input {
    color: #ffffff !important;
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

/* Placeholder */

div[data-baseweb="input"] input::placeholder {
    color: #9ca3af !important;
}

/* Selectbox */

div[data-baseweb="select"] span {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------

st.markdown(
"<h1 style='text-align:center;'>AI Branding Studio</h1>",
unsafe_allow_html=True
)

st.markdown(
"<p style='text-align:center;'>Generate brand names, slogans and logos instantly</p>",
unsafe_allow_html=True
)

# -------------------------
# Business Idea
# -------------------------

st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

idea = st.text_input(
    "Describe your business idea",
    placeholder="Example: a coffee shop selling buns and chai"
)

if st.button("Generate Brand Names") and idea:

    with st.spinner("Generating brand names..."):

        prompt = f"""
Suggest 5 creative brand names.

Return only the names.
One name per line.

Business:
{idea}
"""

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a branding expert"},
                {"role":"user","content":prompt}
            ],
            temperature=0.8
        )

        st.session_state.brand_names = response.choices[0].message.content.strip()

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Brand Names
# -------------------------

if "brand_names" in st.session_state:

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.subheader("Brand Names")

    st.success(st.session_state.brand_names)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Slogan Generator
# -------------------------

if idea and "brand_names" in st.session_state:

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.subheader("Generate Slogans")

    brand_names_list = [
        name.replace("*","").strip()
        for name in st.session_state.brand_names.split("\n")
        if len(name.strip()) > 2
    ]

    selected_name = st.selectbox(
        "Select brand name",
        brand_names_list
    )

    st.session_state.selected_name = selected_name

    if st.button("Generate Slogans"):

        slogan_prompt = f"""
Write 3 short catchy slogans for "{selected_name}"

Business:
{idea}
"""

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a branding expert"},
                {"role":"user","content":slogan_prompt}
            ]
        )

        slogans = response.choices[0].message.content

        st.success("Slogans")
        st.write(slogans)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Logo Generator
# -------------------------

if idea and "selected_name" in st.session_state:

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.subheader("Generate Logo")

    logo_style = st.text_input(
        "Logo style",
        "modern minimalist flat vector logo"
    )

    if st.button("Generate Logo"):

        with st.spinner("Creating logo..."):

            image_prompt = f"""
Professional logo design.

Brand: {st.session_state.selected_name}

Business:
{idea}

Style:
{logo_style}

clean vector logo
minimal startup branding
centered icon
white background
"""

            result = openai.images.generate(
                model="gpt-image-1",
                prompt=image_prompt,
                size="1024x1024",
                quality="high"
            )

            img = result.data[0]

            if img.url:

                st.image(img.url, width=350)

                st.download_button(
                    label="Download Logo",
                    data=img.url,
                    file_name="logo.png"
                )

            elif img.b64_json:

                image_bytes = base64.b64decode(img.b64_json)

                st.image(image_bytes, width=350)

                st.download_button(
                    label="Download Logo",
                    data=image_bytes,
                    file_name="logo.png"
                )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------

st.markdown(
"<p style='text-align:center;opacity:0.6;'>Built with OpenAI and Streamlit</p>",
unsafe_allow_html=True
)