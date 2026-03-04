import streamlit as st

def generate_ai_response(country, growth, inflation):

    if growth > 5 and inflation < 6:
        status = "High Growth & Stable Economy"
        strategy = "Aggressive export expansion recommended."
    elif inflation > 8:
        status = "High Inflation Risk"
        strategy = "Adopt cautious export strategy."
    else:
        status = "Moderate Opportunity"
        strategy = "Balanced expansion approach suggested."

    return f"""
### 🤖 AI Executive Insight

Country: **{country}**

Growth: {growth:.2f}%
Inflation: {inflation:.2f}%

Market Status: **{status}**

Strategy Recommendation:
{strategy}
"""


def chatbot_ui(country,growth,inflation):
    st.subheader("🤖 AI Chatbot")
    q=st.text_input("Ask something")
    if q:
        st.write(f"{country} growth is {growth:.2f}% with inflation {inflation:.2f}%.")