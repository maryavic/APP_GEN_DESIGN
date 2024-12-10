import streamlit as st
import random
from keywords_extractor import KeywordsExtractor
from image_generator import ImageGenerator
import io

def main():
    st.title("🎨 Unified Design Flow: From Sketch to Artwork")
    
    # API Key Input
    stability_api_key = st.sidebar.text_input("Stability AI API Key", type="password")
    
    if not stability_api_key:
        st.warning("Please enter your Stability AI API Key")
        return

    # Initialize the Keyword Extractor and Image Generator
    keyword_extractor = KeywordsExtractor()
    image_generator = ImageGenerator(stability_api_key)

    # Upload Sketch
    st.header("1. Upload Sketch")
    uploaded_image = st.file_uploader("Upload a Sketch (JPG, PNG, JPEG)", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Sketch", use_column_width=True)
        
        # Extract Keywords
        if st.button("Extract Keywords"):
            with st.spinner("Extracting Keywords..."):
                keywords = keyword_extractor.extract_keywords_from_image(uploaded_image)
                
                if keywords:
                    st.session_state.keywords = keywords
                    st.write("### Extracted Keywords: ")
                    st.write(", ".join(keywords))
                    
                    # Generate Prompt
                    st.header("2. Generate Prompt from Keywords")
                    prompt = image_generator.generate_prompt(keywords)
                    st.session_state.prompt = prompt
                    st.write("Generated Prompt:", prompt)
        
        # Generate Image if Prompt and Keywords are available
        if 'prompt' in st.session_state and 'keywords' in st.session_state:
            st.header("3. Generate Artwork")
            col1, col2 = st.columns(2)
            with col1:
                cfg_scale = st.slider("Guidance Scale", 1, 20, 7)
            with col2:
                steps = st.slider("Diffusion Steps", 10, 150, 50)
            
            seed = st.number_input("Random Seed", value=random.randint(0, 2**32 - 1))
            
            if st.button("Generate Artwork"):
                with st.spinner("Generating Artwork..."):
                    generated_image = image_generator.generate_image(
                        st.session_state.prompt,
                        seed=seed,
                        cfg_scale=cfg_scale,
                        steps=steps
                    )
                    
                    if generated_image:
                        st.image(generated_image, caption="Generated Artwork")
                        
                        # Download Option
                        img_byte_arr = io.BytesIO()
                        generated_image.save(img_byte_arr, format='PNG')
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        st.download_button(
                            label="Download Artwork",
                            data=img_byte_arr,
                            file_name="generated_artwork.png",
                            mime="image/png"
                        )
                    else:
                        st.error("Image generation failed. Please try again.")
    else:
        st.warning("Please upload a sketch first.")

if __name__ == "__main__":
    main()
