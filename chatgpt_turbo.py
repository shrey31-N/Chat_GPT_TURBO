import streamlit as st
from openai import OpenAI
import openai

client = OpenAI(api_key="your API key")

st.title("Chat with ChatGPT Turbo")
st.subheader("Chat")

if 'hst_conversation' not in st.session_state:
    st.session_state.hst_conversation = []

question = st.text_input("Enter your question:")
btn_send = st.button("Send Question")

if btn_send and question:
    st.session_state.hst_conversation.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.hst_conversation,
            max_tokens=500
        )
        answer = response.choices[0].message.content
        st.session_state.hst_conversation.append({"role": "assistant", "content": answer})

    except openai.RateLimitError as e:
        st.error("⚠️ Rate limit exceeded or insufficient quota. Please check your billing details at https://platform.openai.com/account/billing")
    except openai.AuthenticationError as e:
        st.error("❌ Invalid API key. Please verify your key.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Display the chat
for msg in st.session_state.hst_conversation:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")
