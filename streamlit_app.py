import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable or Streamlit secrets
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY") or st.secrets.get("TOGETHER_API_KEY", "")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
# Using Mistral 7B model which is more lightweight and works well for paraphrasing
TOGETHER_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

# Set page configuration
st.set_page_config(
    page_title="Academic Paraphraser",
    page_icon="🔄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        margin-bottom: 0;
    }
    .subheader {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .stButton button {
        width: 100%;
    }
    .output-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #e7f5ff;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #b8daff;
        margin-bottom: 20px;
    }
    .result-text {
        white-space: pre-wrap;
        font-size: 16px;
        line-height: 1.6;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("<h1 class='main-header'>Academic Paraphraser</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>by Shem Escobal - Paraphrase academic text naturally</p>", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Settings")
    
    # Academic level selection
    academic_level = st.selectbox(
        "Academic Level",
        ["High-School", "Undergraduate", "Graduate", "Ph.D."],
        index=1
    )
    
    # Tips section
    st.markdown("### Tips")
    st.markdown("""
    - Paste your academic text in the editor
    - Select the appropriate academic level
    - Click "Paraphrase" to generate a new version
    - The paraphrased text will be natural and concise
    - Review and edit the result as needed
    """)
    
    # Info box
    st.markdown("""
    <div class='info-box'>
        <b>📝 Note:</b> This tool helps with paraphrasing while maintaining academic integrity. 
        Always review the output and cite your sources properly.
    </div>
    """, unsafe_allow_html=True)
    
    # Test API connection
    if st.button("Test API Connection"):
        with st.spinner("Testing API connection..."):
            try:
                # Make a simple request to the models endpoint to verify API key
                response = requests.get(
                    "https://api.together.xyz/v1/models",
                    headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    st.success("API key is valid and connection to Together AI is working!")
                elif response.status_code == 401:
                    st.error("Authentication error: Your API key is invalid or expired.")
                else:
                    st.error(f"Unexpected status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error testing API: {str(e)}")

with col2:
    st.markdown("### Original Text")
    original_text = st.text_area(
        "Paste your academic text here",
        height=200,
        key="original_text",
        help="Paste the text you want to paraphrase here"
    )
    
    # Word count
    if original_text:
        word_count = len(original_text.split())
        st.caption(f"{word_count} words")
    
    # Create a container for results
    result_container = st.container()
    
    # Paraphrase button
    if st.button("Paraphrase", type="primary"):
        if not original_text:
            st.error("Please enter some text to paraphrase.")
        elif not TOGETHER_API_KEY:
            st.error("API key not configured. Please set the TOGETHER_API_KEY environment variable or in Streamlit secrets.")
        else:
            with st.spinner("Generating paraphrased text..."):
                try:
                    # Prepare the prompt for Together AI with improved instructions
                    prompt = f"""Paraphrase the following academic text to maintain the same meaning but with different wording. 
                    
                    Guidelines:
                    - Make it sound natural and appropriate for {academic_level} level academic writing
                    - Avoid overly formal or verbose language
                    - Keep the paraphrased text concise and clear
                    - Don't add unnecessary explanations or notes
                    - Don't include placeholders like "(Author's Last Name, Year)" unless they're in the original text
                    - Focus on rewording while preserving the original meaning and tone.
                    - In academic writing, contractions (e.g., it’s instead of it is, can’t instead of cannot) should generally be avoided to maintain a formal tone.
                    
                    Original text: {original_text}
                    
                    Paraphrased text:"""
                    
                    # Call Together AI API
                    response = requests.post(
                        TOGETHER_API_URL,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {TOGETHER_API_KEY}"
                        },
                        json={
                            "model": TOGETHER_MODEL,
                            "messages": [
                                {"role": "system", "content": "You are an academic writing assistant that specializes in paraphrasing text while maintaining academic integrity. Just produce only the paraphrased text, no other text or notes."},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 2000
                        },
                        timeout=60
                    )
                    
                    # Handle authentication errors
                    if response.status_code == 401:
                        st.error("Authentication error: Your API key is invalid or expired.")
                        st.stop()
                    
                    # Check if response is successful
                    response.raise_for_status()
                    
                    response_data = response.json()
                    
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        # Extract the content from the message
                        paraphrased_text = response_data['choices'][0]['message']['content'].strip()
                        
                        # Clean up any extra notes or explanations that might be added
                        if "Note:" in paraphrased_text:
                            paraphrased_text = paraphrased_text.split("Note:")[0].strip()
                        if "Alternatively:" in paraphrased_text:
                            paraphrased_text = paraphrased_text.split("Alternatively:")[0].strip()
                        
                        # Display the result in the container
                        with result_container:
                            st.markdown("### Paraphrased Text")
                            
                            # Create a text area for the paraphrased text that serves both display and copy purposes
                            st.text_area(
                                "",  # No label needed as we already have the header
                                value=paraphrased_text,
                                height=200,
                                key="paraphrased_output"
                            )
                            
                            # Add a copy button
                            if st.button("Copy to Clipboard"):
                                st.success("Text copied to clipboard!")
                                st.markdown(
                                    f"""
                                    <script>
                                        navigator.clipboard.writeText(`{paraphrased_text.replace('`', '\\`')}`);
                                    </script>
                                    """,
                                    unsafe_allow_html=True
                                )
                    else:
                        error_msg = "Failed to get proper response from API"
                        if 'error' in response_data:
                            error_msg += f": {response_data['error'].get('message', '')}"
                        st.error(error_msg)
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"API request error: {str(e)}")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "Created by Shem Escobal | Powered by Together AI | "
    "[Documentation](https://docs.together.ai/reference/chat-completions-1)"
) 
