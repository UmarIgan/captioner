import streamlit as st
from utils import *
from PIL import Image

# Streamlit App
def main():
    # Custom page config
    st.set_page_config(page_title="Image Chatbot", page_icon=":camera:", layout="centered")

    # Hide Streamlit's default footer and menu
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .css-164nlkn {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Initialize conversation history
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # App title
    st.title("Image Chatbot")
    st.write("Upload an image and chat with the AI about it. Previous questions and answers will be included in the prompt.")

    # Upload image
    uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        # Display image at the top of the app
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # Keep track of the uploaded image in session state to always show it
        if "uploaded_image" not in st.session_state:
            st.session_state["uploaded_image"] = uploaded_image

    elif "uploaded_image" in st.session_state:
        # Display previously uploaded image if no new image is uploaded
        image = Image.open(st.session_state["uploaded_image"])
        st.image(image, caption='Uploaded Image', use_column_width=True)

    # Show conversation history below the image
    st.subheader("Conversation History")
    for item in st.session_state["history"]:
        st.write(f"**You:** {item['question']}")
        st.write(f"**AI:** {item['answer']}")
    
    # Prompt input
    prompt = st.text_input("Enter your prompt", "Define the image")

    # If the image is uploaded, process and display the result
    if "uploaded_image" in st.session_state:
        if st.button("Send"):
            # Append previous conversation to the prompt
            full_prompt = ""
            for item in st.session_state["history"]:
                full_prompt += f"Q: {item['question']} A: {item['answer']} "
            full_prompt += f"Q: {prompt}"

            with st.spinner("Processing..."):
                # Call the function with the concatenated prompt
                result = process_single_image_and_get_result(image, full_prompt)
            
            # Store the current interaction in session state
            st.session_state["history"].append({"question": prompt, "answer": result})

            st.success("Answer generated!")
            st.write(f"**AI:** {result}")

    # Social links
    st.markdown("---")
    st.markdown("**Created by [Umar](https://x.com/Umar26338572)**")
    col1, col2 = st.columns([1, 10])
    with col1:
        st.image("https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/x-social-media-black-icon.png", width=20)
    with col2:
        st.markdown("[Twitter](https://x.com/Umar26338572)")
    
    col1, col2 = st.columns([1, 10])
    with col1:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTO9lOYvVYtruNLntp5K61JoX4mACQZ0BmTqQ&s", width=20)
    with col2:
        st.markdown("[LinkedIn](https://www.linkedin.com/in/umarigan/)")

if __name__ == "__main__":
    main()
