import streamlit as st
from agent import get_agent_response

st.set_page_config(page_title="CLV Predictor & Campaign Agent", layout="centered")

st.title("Customer Value Predictor & Campaign Writer Agent")
st.write("Predict future 90-day Customer Lifetime Value (CLV), receive optimal send-time windows, and generate personalized campaign emails.")

col1, col2 = st.columns(2)
with col1:
    recency_days = st.number_input("Days Since Last Purchase", min_value=1, max_value=365, value=15)
    frequency_orders = st.number_input("Total Orders (Frequency)", min_value=1, max_value=100, value=5)

with col2:
    hist_monetary = st.number_input("Total Historical Spend ($)", min_value=5.0, max_value=10000.0, value=450.0)
    avg_order_value = st.number_input("Avg Order Value ($)", min_value=5.0, max_value=2000.0, value=90.0)

if st.button("Predict CLV & Generate Campaign"):
    with st.spinner("Processing prediction and querying campaign agent..."):
        try:
            clv, tier, campaign_copy = get_agent_response(recency_days, frequency_orders, hist_monetary, avg_order_value)
            
            st.divider()
            st.metric(label="Predicted Future 90-Day CLV", value=f"${clv:.2f}")
            
            if tier == "VIP High Value":
                st.success(f"Segment: {tier}")
            elif tier == "Mid-Tier Regular":
                st.info(f"Segment: {tier}")
            else:
                st.warning(f"Segment: {tier}")
                
            st.subheader("AI Agent Strategy & Campaign Copy")
            st.markdown(campaign_copy)
        except Exception as e:
            st.error(f"Error executing agent request: {str(e)}")