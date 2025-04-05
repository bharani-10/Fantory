import streamlit as st
import google.generativeai as genai
import random

# --- Gemini Setup ---
genai.configure(api_key="AIzaSyCa3Ag32NQUlkbe5LEwEH67z08uPNT4hYg")  # Replace with your API key
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Streamlit UI ---
st.set_page_config(
    page_title="✨ Magic Story Wizard", 
    page_icon="🧙‍♂️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for the app - simpler approach that works reliably with Streamlit
st.markdown("""
    <style>
    /* Set the page background */
    .stApp {
        background-color: #000000;
    }
    
    /* Header styling */
    .header {
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Title styling */
    .title {
        font-size: 3rem;
        font-weight: bold;
        color: #FFD700;
        text-shadow: 0 0 10px #FF8C00, 0 0 20px #FF8C00;
        margin-bottom: 10px;
        background: linear-gradient(90deg, rgba(255,215,0,0) 0%, rgba(255,215,0,0.3) 50%, rgba(255,215,0,0) 100%);
        padding: 10px;
        border-radius: 20px;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1.5rem;
        color: #FF8C00;
        margin-bottom: 10px;
    }
    
    /* Input field */
    .stTextInput > div > div > input {
        background-color: #1E1E3A;
        color: white;
        border: 2px solid #9370DB;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 18px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #9370DB, #FF8C00);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        font-size: 1.2rem;
        margin-top: 10px;
    }
    
    .stButton > button:hover {
        filter: brightness(1.2);
    }
    
    /* Story box */
    .story-container {
        background: linear-gradient(145deg, #111122, #1E1E3A);
        border: 3px solid #9370DB;
        border-radius: 15px;
        padding: 25px;
        margin-top: 20px;
        color: #E0E0FF;
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.3);
    }
    
    .story-title {
        font-size: 2rem;
        color: #FFD700;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0 0 5px #FF8C00;
    }
    
    .story-content {
        font-size: 1.2rem;
        line-height: 1.6;
        color: #E0E0FF;
    }
    
    /* Make all text light colored */
    p, div {
        color: #E0E0FF !important;
    }
    
    /* Decorate corners with emoji */
    .corner-decoration {
        font-size: 2.5rem;
        position: fixed;
        z-index: 1;
    }
    
    .top-left {
        top: 20px;
        left: 20px;
    }
    
    .top-right {
        top: 20px;
        right: 20px;
    }
    
    .bottom-left {
        bottom: 20px;
        left: 20px;
    }
    
    .bottom-right {
        bottom: 20px;
        right: 20px;
    }
    
    /* Custom color for warnings */
    div[data-testid="stAlert"] {
        background-color: rgba(255, 140, 0, 0.2);
        color: #FFD700 !important;
        border: 1px solid #FF8C00;
    }
    </style>
    
    <!-- Corner decorations -->
    <div class="corner-decoration top-left">✨</div>
    <div class="corner-decoration top-right">🌟</div>
    <div class="corner-decoration bottom-left">🔮</div>
    <div class="corner-decoration bottom-right">🪄</div>
    
    <!-- Header with title and subtitle -->
    <div class="header">
        <div class="title">✨ Magic Story Wizard ✨</div>
        <div class="subtitle">Tell me your wish for a wondrous tale!</div>
    </div>
""", unsafe_allow_html=True)

# Create three columns for layout
left_col, main_col, right_col = st.columns([1, 3, 1])

with left_col:
    st.markdown('<div style="font-size: 5rem; text-align: center; margin-top: 50px;">🧙‍♂️</div>', unsafe_allow_html=True)

with main_col:
    # User input
    user_prompt = st.text_input("What magical adventure shall we imagine?", 
                             placeholder="e.g. A princess with magical shoes...")
    
    # Generate story button
    if st.button("✨ Weave My Story! ✨"):
        if not user_prompt.strip():
            st.warning("Please tell me what kind of story you want!")
        else:
            with st.spinner("Casting a spell to create your story..."):
                try:
                    # Enhanced prompt for child-friendly story
                    enhanced_prompt = f"""
Write a engaging, age-appropriate fantasy story for children **strictly** based on this idea: "{user_prompt}".  
Do **not** add your own ideas or recommendations.  
Stay fully aligned with the concept provided. Provide the complete story
Start with a title on its own line.
"""

                    
                    response = model.generate_content(enhanced_prompt)
                    story = response.text
                    
                    # Parse title and content
                    story_lines = story.split('\n')
                    title = story_lines[0].replace('#', '').strip()
                    # If the title is too long, it's probably not a title
                    if len(title) > 50 or title == '':
                        title = "Your Magical Story"
                        story_content = story
                    else:
                        # Remove the title from the story content
                        story_content = '\n'.join(story_lines[1:]).strip()
                    
                    # Display story
                    st.markdown(f"""
                    <div class="story-container">
                        <div class="story-title">{title}</div>
                        <div class="story-content">{story_content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Save for later
                    st.session_state["story"] = story
                    st.session_state["story_title"] = title
                    
                except Exception as e:
                    st.error(f"Our magic wand fizzled! Let's try again! ({e})")

with right_col:
    st.markdown('<div style="font-size: 5rem; text-align: center; margin-top: 50px;">✨</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px;">
    <div style="font-size: 1.5rem; margin-bottom: 10px; color: #9370DB;">
        ✨ 🌟 ✨ 🌟 ✨
    </div>
    <div style="font-size: 1rem; color: #9370DB;">
        Created with magic for young storytellers
    </div>
</div>
""", unsafe_allow_html=True)