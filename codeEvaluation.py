import streamlit as st
import google.generativeai as genai
import PIL.Image
import os

# Configure Gemini API key
GEMINI_API_KEY = "AIzaSyCeeQH5t2hAOkr6kZBPklGaaTcLnNeg_Rw"
genai.configure(api_key=GEMINI_API_KEY)

# Function to analyze text-based code
def analyze_text_code(code):
    prompt = f"""
    Review the following code and provide concise suggestions in 4 sentences.
    Also, give a score out of 10.
    
    Code:
    {code}
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use gemini-1.5-pro for higher accuracy
    response = model.generate_content(prompt)
    return response.text if response else "No response received."

# Function to analyze image-based code
def analyze_image_code(image_path):
    image = PIL.Image.open(image_path)
    prompt = "Analyze the handwritten or printed code in this image. Provide 4 concise improvement suggestions and give a score out of 10."
    
    model = genai.GenerativeModel("gemini-1.5-pro")  # Supports image input
    response = model.generate_content([prompt, image])
    
    return response.text if response else "No response received."

# Streamlit UI
st.title("🔍 Code Checker using Gemini API")

uploaded_file = st.file_uploader("Upload a code file (text or image)", type=["py", "txt", "jpg", "png", "jpeg"])

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()

    if file_ext in [".py", ".txt"]:  # Text-based code
        code = uploaded_file.getvalue().decode("utf-8")
        st.code(code, language="python")
        st.write("🧠 Analyzing code...")
        result = analyze_text_code(code)
    elif file_ext in [".jpg", ".png", ".jpeg"]:  # Image-based code
        image_path = f"temp_image{file_ext}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(uploaded_file, caption="📸 Uploaded Code Image", use_column_width=True)
        st.write("🧠 Analyzing handwritten/printed code...")
        result = analyze_image_code(image_path)
        os.remove(image_path)  # Cleanup
    else:
        st.error("❌ Unsupported file format.")
        result = None

    if result:
        st.subheader("📋 Analysis Results:")
        st.write(result)