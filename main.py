import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Playground",
    layout="centered"
)

st.title("Playground")

st.markdown(
    "Enter your Gemini API key, choose a model, tune generation settings, and generate a response."
)

st.sidebar.header("Configuration")

api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password"
)

model_name = st.sidebar.selectbox(
    "Gemini Model",
    [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-3-pro-preview",
    ]
)

st.sidebar.header("Generation Settings")

temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.95, 0.01)
top_k = st.sidebar.slider("Top-k", 1, 100, 40, 1)
max_output_tokens = st.sidebar.slider("Max Output Tokens", 64, 8192, 1024, 64)

st.subheader("Prompt")

prompt = st.text_area(
    "Enter your prompt",
    height=200
)

generate_clicked = st.button("Generate Response", use_container_width=True)

if generate_clicked:
    if not api_key:
        st.error("API key is required.")
    elif not prompt.strip():
        st.error("Prompt is required.")
    else:
        try:
            client = genai.Client(api_key=api_key)

            generation_config = types.GenerateContentConfig(
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                max_output_tokens=max_output_tokens,
            )

            st.subheader("Response")
            output_placeholder = st.empty()
            full_text = ""

            stream = client.models.generate_content_stream(
                model=model_name,
                contents=prompt,
                config=generation_config,
            )

            for event in stream:
                if event.candidates:
                    for part in event.candidates[0].content.parts:
                        if hasattr(part, "text") and part.text:
                            full_text += part.text
                            output_placeholder.markdown(full_text)
            print(full_text)

        except Exception as e:
            st.error(str(e))

st.markdown("---")
st.caption("Built with Streamlit and Google Gemini")

