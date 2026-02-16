import streamlit as st
import openai
import requests
import json

# ---------- CONFIGURATION ----------
# මෙතන API Keys ටික ඔයාගේ Streamlit Secrets වලට දාන්න
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"] 

st.set_page_config(page_title="BLACK HAT SCRIPT FIXER", layout="wide")

# Custom UI Styling (Black & Orange Neon)
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ff8800; }
    .stTextArea textarea { 
        background-color: #000; color: #00ff00; 
        border: 2px solid #ff4400; font-family: 'Courier New', monospace;
    }
    .stButton>button { 
        background: linear-gradient(45deg, #ff4400, #ff8800); 
        color: black; font-weight: bold; border: none; padding: 12px;
        border-radius: 5px; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); background: #ffffff; }
    h1 { color: #ff4400; text-shadow: 0px 0px 15px #ff4400; text-align: center; font-size: 3rem; }
    .stCodeBlock { border: 1px solid #ff4400 !important; }
</style>
""", unsafe_allow_html=True)

# ---------- CORE FUNCTIONS ----------

def search_advanced_solutions(error_query):
    """Google Search through Serper.dev for real-time context"""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": f"python fix error {error_query}"})
    headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=payload)
        results = response.json().get('organic', [])
        return " ".join([res.get('snippet', '') for res in results[:2]])
    except:
        return "No additional web context found."

def fix_script_with_groq(original_code, context):
    """Fix code using Groq (llama-3.1-70b-versatile)"""
    # Groq පාවිච්චි කරද්දී base_url එක වෙනස් විය යුතුයි
    client = openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY
    )
    
    prompt = f"""
    SYSTEM: You are an elite Security Researcher and Python Architect. 
    WEB CONTEXT: {context}
    
    USER SCRIPT:
    {original_code}
    
    TASK:
    1. Fix all syntax, logic, and indentation errors.
    2. Optimize for high-speed execution.
    3. If the script is a tool, convert it into a professional Streamlit web app.
    4. Provide ONLY the clean, ready-to-run Python code. 
    5. No explanations, no markdown backticks.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2 # නිරවද්‍යතාව වැඩි කිරීමට
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq: {str(e)}"

# ---------- MAIN INTERFACE ----------
st.markdown("<h1>🔥 BLACK HAT SCRIPT FIXER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666;'>Powered by Groq Llama-3.1 & Serper Intel</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 BROKEN TERMINAL")
    user_code = st.text_area("Paste code here...", height=450, placeholder="# Wait for input...")
    
    if st.button("EXECUTE RECONSTRUCTION"):
        if user_code:
            with st.spinner("🛠️ RECONSTRUCTING SCRIPT AT HYPER-SPEED..."):
                # Step 1: Search Web
                web_info = search_advanced_solutions(user_code[:150])
                # Step 2: Fix with Groq
                fixed_result = fix_script_with_groq(user_code, web_info)
                # Clean markdown tags if AI includes them
                clean_code = fixed_result.replace("```python", "").replace("```", "").strip()
                st.session_state.final_output = clean_code
        else:
            st.warning("Input is empty. Enter a script to proceed.")

with col2:
    st.subheader("⚡ OPTIMIZED OUTPUT")
    if 'final_output' in st.session_state:
        st.code(st.session_state.final_output, language="python")
        
        st.download_button(
            label="📥 DOWNLOAD RECONSTRUCTED SCRIPT",
            data=st.session_state.final_output,
            file_name="fixed_tool_pro.py",
            mime="text/x-python"
        )
        
        st.success("SYSTEM READY: 100% OPTIMIZED")
        st.info("DEPLOYMENT: Run 'streamlit run fixed_tool_pro.py' to launch.")
    else:
        st.info("Output will be displayed here after execution.")

st.markdown("---")
st.markdown("<p style='text-align:center; font-family:monospace;'>[ STATUS: SYSTEM ONLINE ]</p>", unsafe_allow_html=True)
