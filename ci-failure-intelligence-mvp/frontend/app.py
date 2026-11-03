import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT",
    "gpt-4.1"
)

PROVIDER_NAME = "Azure OpenAI"
import streamlit as st, requests
API_URL='http://localhost:9000'
st.set_page_config(page_title='CI Failure Intelligence Copilot',page_icon='🤖',layout='wide')
st.title("🤖 CI Failure Intelligence Copilot")

st.caption(
    f"Powered by {PROVIDER_NAME} • {MODEL_NAME}"
)
if 'messages' not in st.session_state: st.session_state.messages=[]
if 'analysis' not in st.session_state: st.session_state.analysis=None
with st.sidebar:
    st.header("AI Configuration")

    st.success("🟢 Connected")

    st.metric(
        "Model",
        MODEL_NAME
    )

    st.caption(PROVIDER_NAME)

    st.divider()    
    st.header('Context')
    uploaded=st.file_uploader('📎 Attach Build Log',type=['log','txt'])
    if uploaded and st.button('Analyze Log'):
        log_text=uploaded.read().decode()
        data=requests.post(f'{API_URL}/analyze',json={'log':log_text},timeout=180).json()
        st.session_state.analysis=data
        st.session_state.messages.append({'role':'assistant','content':f"Analysis completed. Root cause: {data.get('root_cause','N/A')}"})
    if st.session_state.analysis:
        st.divider()
        st.write('Current RCA')
        st.json(st.session_state.analysis)
for m in st.session_state.messages:
    with st.chat_message(m['role']): st.markdown(m['content'])
q=st.chat_input('Ask about CI failures, Kubernetes, OOM, test failures...')
if q:
    st.session_state.messages.append({'role':'user','content':q})
    if st.session_state.analysis:
        ans=requests.post(f'{API_URL}/chat',json={'analysis':st.session_state.analysis,'question':q},timeout=180).json()['answer']
    else:
        ans=requests.post(f'{API_URL}/general-chat',json={'question':q},timeout=180).json()['answer']
    st.session_state.messages.append({'role':'assistant','content':ans})
    st.rerun()
