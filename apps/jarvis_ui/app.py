import streamlit as st
import httpx

st.set_page_config(page_title="ipe — Jarvis", layout="wide")
st.title("ipe — Jarvis")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for m in st.session_state["messages"]:
    st.chat_message(m["role"]).write(m["content"])

u = st.chat_input("Bir şey yaz...")
if u:
    st.session_state["messages"].append({"role": "user", "content": u})
    try:
        r = httpx.post("http://localhost:8000/api/directive", json={"text": u}, timeout=10).json()
        msg = r.get("message") or r
    except Exception as e:
        msg = f"Hata: {e}"
    st.session_state["messages"].append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

st.sidebar.header("Paneller")
st.sidebar.write("- Mentor Log (yakında)")
st.sidebar.write("- Manuel Adımlar (Maps / Lens)")
