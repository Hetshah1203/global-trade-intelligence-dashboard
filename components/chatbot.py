import streamlit as st

def chatbot():

    st.subheader("🤖 Trade AI Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    user_input=st.text_input("Ask trade question")

    if user_input:
        response=f"""
Based on AI trade analytics:
Consider markets with high demand and low tariff barriers.
Diversification across regions improves export stability.
"""

        st.session_state.messages.append(("You",user_input))
        st.session_state.messages.append(("AI",response))

    for role,msg in st.session_state.messages:
        st.write(f"**{role}:** {msg}")