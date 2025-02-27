import streamlit as st
import requests
import io
from PIL import Image
from datetime import datetime
import time
import urllib.parse

st.set_page_config(
    page_title="AI Beautician Art Generator",
    page_icon="💄",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        color: #E91E63;
    }
    .stButton>button {
        width: 100%;
        background-color: #E91E63;
        color: white;
    }
    .api-badge {
        background-color: #f0f2f6;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.8em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>💄 AI Beautician Art Generator</h1>", unsafe_allow_html=True)
st.markdown("### Create stunning beauty transformations using AI! ✨")

# Input fields
prompt = st.text_area("Describe the beauty transformation:", placeholder="Example: A glamorous bridal makeup with elegant eyeliner and rosy cheeks")

col1, col2, col3 = st.columns(3)
with col1:
    style = st.selectbox(
        "Choose Beauty Style:",
        ["Bridal Makeup", "Natural Look", "Glamorous", "Korean Glass Skin", "Fantasy Makeup", "Cyberpunk Look", "Vintage Beauty"]
    )
with col2:
    quality = st.select_slider(
        "Image Quality:",
        options=["Standard", "High", "Ultra"],
        value="High"
    )
with col3:
    api_choice = st.selectbox(
        "API Source:",
        ["Auto (Recommended)", "Pollinations", "Craiyon", "Stable Diffusion"]
    )

# Initialize session state
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []
if 'total_generated' not in st.session_state:
    st.session_state.total_generated = 0

# Function to generate beautician art
def generate_beauty_art(prompt, style):
    try:
        base_url = "https://image.pollinations.ai/prompt/"
        enhanced_prompt = f"{style}, {prompt}, beauty portrait, high quality, elegant makeup, professional lighting"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        image_url = f"{base_url}{encoded_prompt}"
        
        response = requests.get(image_url, timeout=15)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content)), None
        else:
            return None, f"Error: {response.status_code}"
    except Exception as e:
        return None, str(e)

# Generate button
if st.button("💄 Generate Beauty Art"):
    if not prompt:
        st.error("Please enter a description for the beauty transformation!")
    else:
        with st.spinner("💄 Creating your beauty masterpiece..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress_bar.progress(i + 1)
            
            if quality == "High":
                prompt += ", high quality, detailed"
            elif quality == "Ultra":
                prompt += ", ultra high quality, extremely detailed, 4K, professional"
            
            generated_image, error = generate_beauty_art(prompt, style)
            
            if error:
                st.error(f"Generation failed: {error}")
                st.info("Please try again with a different prompt or style.")
            elif generated_image:
                st.session_state.generated_images.append({'image': generated_image, 'prompt': prompt, 'style': style})
                st.session_state.total_generated += 1
                
                st.image(generated_image, caption=f"{style} style beauty transformation", use_column_width=True)

                img_bytes = io.BytesIO()
                generated_image.save(img_bytes, format='PNG')
                st.download_button(
                    label="📥 Download Beauty Art",
                    data=img_bytes.getvalue(),
                    file_name=f"beauty_art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )
                st.success(f"✨ Beauty Art #{st.session_state.total_generated} generated successfully!")

# Display history
if st.session_state.generated_images:
    with st.expander("💄 Your Generated Beauty Arts"):
        for idx, item in enumerate(reversed(st.session_state.generated_images[-10:])):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.image(item['image'], caption=f"Beauty Art #{len(st.session_state.generated_images)-idx}", width=300)
            with col2:
                st.write(f"**Prompt:** {item['prompt']}")
                st.write(f"**Style:** {item['style']}")

# File Upload Section
st.markdown("## 📤 Upload Your Own Image")
uploaded_file = st.file_uploader("Upload an image to enhance with AI beautician styles:", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded successfully! You can now apply transformations.")
    