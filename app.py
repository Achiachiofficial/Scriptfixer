import streamlit as st
import openai
import google.generativeai as genai
from anthropic import Anthropic
import time
import re

# ---------- PAGE CONFIG (DARK THEME FORCE) ----------
st.set_page_config(
    page_title="🔥 FIX MY SCRIPT | BLACK HAT EDITION", 
    page_icon="🔥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for DARK THEME (අඳුරුම Theme එක)
st.markdown("""
<style>
    /* Main background - ගින්දරම black */
    .stApp {
        background: #0a0a0a;
        background-image: radial-gradient(#ff4500 0.5px, transparent 0.5px);
        background-size: 30px 30px;
    }
    
    /* Text colors */
    h1, h2, h3, p, li, .stMarkdown {
        color: #ffaa00 !important;
        text-shadow: 0 0 5px #ff4500;
    }
    
    /* Buttons - ගිනිමය button */
    .stButton > button {
        background: linear-gradient(45deg, #ff4500, #ff8c00);
        color: black;
        font-weight: bold;
        border: 2px solid #ffaa00;
        box-shadow: 0 0 15px #ff4500;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #ff8c00, #ff4500);
        box-shadow: 0 0 30px #ffaa00;
        transform: scale(1.02);
    }
    
    /* Code blocks - හරිම නිට්ටාවට පේන්න */
    .stCodeBlock {
        background: #1a1a1a !important;
        border: 2px solid #ff4500;
        border-radius: 10px;
    }
    
    /* Text areas - අඳුරු background */
    .stTextArea textarea {
        background: #1a1a1a !important;
        color: #ffaa00 !important;
        border: 2px solid #ff4500;
        font-family: 'Courier New', monospace;
    }
    
    /* Sidebar - තවත් අඳුරු */
    .css-1d391kg, .css-1lcbmhc {
        background: #000000 !important;
        background-image: linear-gradient(45deg, #1a1a1a 25%, transparent 25%);
        background-size: 40px 40px;
    }
    
    /* Success/Error messages */
    .stAlert {
        background: #1a1a1a !important;
        border: 2px solid #ff4500 !important;
        color: #ffaa00 !important;
    }
    
    /* Headers with fire effect */
    h1 {
        font-size: 3em !important;
        background: linear-gradient(45deg, #ff4500, #ffaa00, #ff4500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px #ff4500;
        animation: fire 2s infinite;
    }
    
    @keyframes fire {
        0% { text-shadow: 0 0 10px #ff4500; }
        50% { text-shadow: 0 0 30px #ffaa00; }
        100% { text-shadow: 0 0 10px #ff4500; }
    }
    
    /* ගිනිමය border for containers */
    div[data-testid="stVerticalBlock"] > div {
        border: 1px solid #ff4500;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        background: rgba(0,0,0,0.7);
        box-shadow: 0 0 20px rgba(255,69,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("# 🔥 BLACK HAT SCRIPT FIXER 🔥")
st.markdown("### *වැඩ නැති script එක දාපන්, මං ගින්දරම කරලා දෙන්නම්*")
st.markdown("---")

# ---------- SIDEBAR - API KEYS & MODEL SELECTION ----------
with st.sidebar:
    st.markdown("## 🔥 API KEYS (දාන්න තියෙන ඒවා දාපන්)")
    st.markdown("---")
    
    # Model selection with FIRE emoji
    model_option = st.selectbox(
        "🔥 MODEL එක තෝරපන් (බ්ලොක් වුණොත් අනිකක් ගනින්)",
        ["OpenAI GPT-4", "OpenAI GPT-3.5", "Google Gemini Pro", "Anthropic Claude", "Local Model (Testing)"]
    )
    
    st.markdown("---")
    
    # Dynamic API key inputs based on selected model
    api_key = None
    if "OpenAI" in model_option:
        api_key = st.text_input("🔑 OpenAI API Key (sk-...)", type="password", placeholder="sk-...")
        st.markdown("💡 ගින්දර key එකක් දාපන්")
    elif "Google" in model_option:
        api_key = st.text_input("🔑 Google API Key", type="password", placeholder="AIza...")
        st.markdown("💡 Gemini key එක දාපන්")
    elif "Anthropic" in model_option:
        api_key = st.text_input("🔑 Claude API Key", type="password", placeholder="sk-ant-...")
        st.markdown("💡 Claude key එක දාපන්")
    else:
        api_key = "local_test"
        st.markdown("💡 Local mode - API key ඕන නෑ")
    
    st.markdown("---")
    st.markdown("### 🔥 SETTINGS")
    
    # Temperature control for creativity
    temperature = st.slider("🌡️ FIRE LEVEL (Temperature)", 0.0, 1.0, 0.3, 0.1)
    
    # Fix level
    fix_level = st.select_slider(
        "⚡ FIX කරන තරම",
        options=["අඩුවෙන්", "මදින් මද", "ගින්දරම", "BLACK HAT"],
        value="ගින්දරම"
    )
    
    st.markdown("---")
    st.markdown("### 📱 PHONE LINK")
    if "share" in st.query_params:
        st.code(f"https://share.streamlit.io/your-app")
    st.markdown("---")

# ---------- MAIN CONTENT ----------
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("## 🐍 ORIGINAL SCRIPT (වැඩ නැති එක)")
    st.markdown("*මෙතන දාපන්, මං හදලා දෙන්නම්*")
    
    # Sample script placeholder
    default_code = """# උදාහරණයක් විදිහට මේ වැඩ නැති code එක දාලා බලපන්
def calc(x y)
    result = x + 
    print result
    return"""
    
    user_script = st.text_area("", default_code, height=300, key="input_script")
    
    # Upload file option
    uploaded_file = st.file_uploader("📂 File එකක් තියෙනවනම් upload කරපන්", type=['py', 'txt'])

with col2:
    st.markdown("## 🔥 FIXED SCRIPT (ගින්දරම)")
    st.markdown("*මේක තමයි හරි ගිය එක*")
    
    fixed_script_placeholder = st.empty()
    
    # Fix button with FIRE
    if st.button("🔥🔥 BLACK HAT FIX කරපන් 🔥🔥", use_container_width=True):
        if not api_key and "Local" not in model_option:
            st.error("🔥 API key එක දාපන්, නැත්නම් වැඩක් නෑ")
        elif not user_script and not uploaded_file:
            st.error("🔥 Script එකක් දාපන්")
        else:
            with st.spinner("🔥 ගින්දරම fix එක කරනවා... ඉවසපන්"):
                try:
                    # Get script content
                    if uploaded_file:
                        script_content = uploaded_file.getvalue().decode()
                    else:
                        script_content = user_script
                    
                    # Create FIRE prompt based on fix level
                    if fix_level == "BLACK HAT":
                        prompt = f"""FIX THIS PYTHON CODE TO BE EXTREMELY FAST AND OPTIMIZED LIKE HELL:
                        - Make it run at maximum speed
                        - Optimize all loops and operations
                        - Remove all bottlenecks
                        - Use fastest possible algorithms
                        - Add error handling that doesn't slow it down
                        - ගින්දරම වේගෙන් වැඩ කරන code එකක් හදන්න
                        
                        ORIGINAL BROKEN CODE:
                        {script_content}
                        
                        RETURN ONLY THE FIXED CODE, NO EXPLANATIONS:"""
                    else:
                        prompt = f"""Fix this Python code. Return only the working code:
                        {script_content}"""
                    
                    # Call appropriate API
                    fixed_code = ""
                    
                    if "OpenAI GPT-4" in model_option:
                        client = openai.OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model="gpt-4",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=temperature
                        )
                        fixed_code = response.choices[0].message.content
                        
                    elif "OpenAI GPT-3.5" in model_option:
                        client = openai.OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=temperature
                        )
                        fixed_code = response.choices[0].message.content
                        
                    elif "Google" in model_option:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content(prompt)
                        fixed_code = response.text
                        
                    elif "Anthropic" in model_option:
                        client = Anthropic(api_key=api_key)
                        response = client.messages.create(
                            model="claude-3-sonnet-20241022",
                            max_tokens=2000,
                            temperature=temperature,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        fixed_code = response.content[0].text
                        
                    else:  # Local mode
                        fixed_code = "# LOCAL MODE: මෙතනින් API call එකක් නෑ\n# ඔයාගේ API key එක දාලා බලපන්\n\n" + script_content
                    
                    # Clean the code (remove markdown code blocks if present)
                    fixed_code = re.sub(r'```python\n?', '', fixed_code)
                    fixed_code = re.sub(r'```\n?', '', fixed_code)
                    
                    # Display fixed code
                    fixed_script_placeholder.code(fixed_code, language="python")
                    
                    # Save to session state for download
                    st.session_state['fixed_code'] = fixed_code
                    
                    # Success message with FIRE
                    st.success("🔥🔥 FIX COMPLETE! ගින්දරම හරි ගියා 🔥🔥")
                    
                except Exception as e:
                    st.error(f"🔥 ERROR: {str(e)}")
                    st.info("💡 වෙනත් model එකක් try කරපන්, සමහරවිට block වෙලා ඇති")
    
    # Download button (appears after fix)
    if 'fixed_code' in st.session_state:
        st.download_button(
            label="📥 FIXED SCRIPT එක DOWNLOAD කරපන්",
            data=st.session_state['fixed_code'],
            file_name="black_hat_fixed.py",
            mime="text/plain",
            use_container_width=True
        )

# ---------- LOCAL HOST LINK & DEPLOYMENT INFO ----------
st.markdown("---")
st.markdown("## 🔗 LOCAL HOST & DEPLOYMENT LINKS")

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("### 🖥️ LOCAL HOST")
    st.code("http://localhost:8501")
    st.markdown("*Terminal එකේ `streamlit run app.py` දාලා run කරපන්*")

with col4:
    st.markdown("### 🚀 GITHUB")
    st.code("git add .\ngit commit -m '🔥 fixer'\ngit push")
    st.markdown("*Code එක push කරපන්*")

with col5:
    st.markdown("### 🌍 VERCEL LINK")
    st.code("https://your-app.vercel.app")
    st.markdown("*මේක phone එකෙන් open කරපන්*")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("### 🔥 BLACK HAT SCRIPT FIXER v1.0 🔥")
st.markdown("*ගින්දරම වැඩ කරන fixer එක | අවුල් තියෙන ඒවා දාපන්, මං හදලා දෙන්නම්*")
st.markdown("---")
