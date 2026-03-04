import streamlit as st

def show_recommendation(trade_score):

    st.subheader("🤖 AI Trade Recommendation")

    if trade_score > 60:
        st.success("✅ HIGHLY RECOMMENDED EXPORT MARKET")
    elif trade_score > 40:
        st.warning("⚠️ MODERATE OPPORTUNITY MARKET")
    else:
        st.error("❌ LOW EXPORT ATTRACTIVENESS")