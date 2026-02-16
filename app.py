import streamlit as st
import openai
import requests
import json

# ---------- CONFIGURATION ----------
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="BLACK HAT SCRIPT FIXER", layout="wide")

# Custom UI Styling
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ff0000; }
    .stTextArea textarea { 
        background-color: #000; color: #00ff00; 
        border: 2px solid #ff0000; font-family: 'Courier New', monospace;
    }
    .stButton>button { 
        background: linear-gradient(45deg, #ff0000, #990000); 
        color: white; font-weight: bold; border: none; padding: 10px;
    }
    h1 { color: #ff0000; text-shadow: 2px 2px #550000; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ---------- CORE FUNCTIONS ----------

def search_advanced_solutions(error_query):
    """Google Search through Serper.dev"""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": f"python fix {error_query} best method"})
    headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=payload)
        return response.json().get('organic', [{}])[0].get('snippet', '')
    except:
        return ""

def fix_script_ai(original_code):
    """Fix code using OpenRouter (Llama 3 70B - High Power)"""
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY
    )
    
    # මෙතන තමයි magic එක තියෙන්නේ. අපි AI එකට කියනවා මේක උපරිමයටම හදන්න කියලා.
    prompt = f"""
    You are an elite software architect and security expert. 
    Analyze and reconstruct this Python script. 
    1. Fix all bugs.
    2. Optimize for maximum performance (High-speed execution).
    3. If it's a tool, enhance it with a clean Streamlit interface.
    
    Code to fix:
    {original_code}
    
    Return ONLY the corrected python code. No chat. No markdown backticks.
    """
    
    response = client.chat.completions.create(
        model="meta-llama/llama-3-70b-instruct:free", # Free model එකක් වුණත් 70B එක පට්ට powerful
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ---------- MAIN INTERFACE ----------
st.title("💀 BLACK HAT SCRIPT RECONSTRUCTOR")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📡 Input Terminal")
    user_code = st.text_area("Enter your broken script or tool logic:", height=400)
    if st.button("EXECUTE RECONSTRUCTION"):
        if user_code:
            with st.spinner("🔍 ANALYZING & SEARCHING SOLUTIONS..."):
                # Search web for context
                web_data = search_advanced_solutions(user_code[:100])
                # Fix via AI
                fixed_code = fix_script_ai(f"Context: {web_data}\nCode: {user_code}")
                st.session_state.final_code = fixed_code
        else:
            st.warning("Please enter some code first!")

with col2:
    st.subheader("⚡ Optimized Output")
    if 'final_code' in st.session_state:
        st.code(st.session_state.final_code, language="python")
        st.download_button("📥 DOWNLOAD FIXED TOOL", st.session_state.final_code, "optimized_tool.py")
        
        # Deployment Link Tip
        st.success("SUCCESS: Script Reconstructed at 100% Efficiency.")
        st.info("Run this locally using: streamlit run optimized_tool.py")
