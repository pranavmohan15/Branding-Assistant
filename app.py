import streamlit as st
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Branding Assistant")

st.title("Branding Assistant")
st.write("Enter your brand name and get a branding idea")

idea = st.text_input("Describe your business idea",
                     placeholder="e.g. A coffee shop that sells coffee and pastries")

# Generate Branding Names
if st.button("Generate Branding Names") and idea:
    with st.spinner("Generating branding names..."):
        prompt = f"Suggest 5 creative, catchy, and relevant brand names for the following business:\n\n{idea}"
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a branding expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=100
            )
            st.session_state.brand_names = response.choices[0].message.content.strip(
            )
            st.success("Here are some brand name ideas:")
            st.write(st.session_state.brand_names)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Slogan Section
if idea and 'brand_names' in st.session_state:
    st.markdown("---")
    st.subheader("📝 Generate Slogans")

    # Let user pick one of the generated names
    brand_names_list = [
        name.strip() for name in st.session_state.brand_names.split("\n") if name.strip()]
    selected_name = st.selectbox(
        "Pick a brand name to generate slogans for:", brand_names_list, key="slogan_select")
    st.session_state.selected_name = selected_name

    if st.button("Generate Slogans") and selected_name:
        with st.spinner("Writing catchy slogans..."):
            slogan_prompt = f"Write 3 short, catchy slogans for a brand named '{selected_name}'. Make sure they align with this business idea: {idea}"
            try:
                slogan_response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system","content": "You are a creative branding expert."},
                        {"role": "user", "content": slogan_prompt}
                    ],
                    temperature=0.8,
                    max_tokens=100
                )
                slogans = slogan_response.choices[0].message.content
                st.success("Here are your slogans:")
                st.write(slogans)
            except Exception as e:
                st.error(f"Error: {e}")

# Logo Section
if idea and 'selected_name' in st.session_state and st.session_state.selected_name:
    st.markdown("---")
    st.subheader("🎨 Generate a Logo with AI")
    logo_style = st.text_input(
        "Describe your logo style (e.g., minimalist, colorful, 3D)", "minimalist, modern")
    if st.button("Generate Logo"):
        with st.spinner("Designing your logo..."):
            image_prompt = f"Logo design for a brand called '{st.session_state.selected_name}'. It should be {logo_style} and reflect this idea: {idea}"
            try:
                dalle_response = openai.images.generate(
                    prompt=image_prompt,
                    n=1,
                    size="512x512"
                )
                image_url = dalle_response.data[0].url
                st.image(image_url, caption="AI-Generated Logo")
            except Exception as e:
                st.error(f"Logo generation failed: {e}")