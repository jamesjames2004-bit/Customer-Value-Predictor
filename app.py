import streamlit as st
from agent import get_agent_response

# 1. Page Configuration & Theme
st.set_page_config(
    page_title="Customer Value Predictor & Campaign Writer",
    page_icon="⚡",
    layout="wide"
)

# Optional Custom CSS for sleek card styling
st.markdown("""
    <style>
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2d3250;
    }
    .main-header {
        font-weight: 700;
        margin-bottom: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Main Title & Subtitle
st.title("⚡ Customer Value Predictor & Campaign Agent")
st.caption("Predict 90-day Customer Lifetime Value (CLV) and automatically generate targeted marketing copy.")

st.divider()

# 3. Sidebar Input Controls
with st.sidebar:
    st.header("📊 Customer Metrics")
    st.write("Enter historical user metrics below:")
    
    recency_days = st.number_input("Days Since Last Purchase", min_value=1, max_value=365, value=15)
    frequency_orders = st.number_input("Total Orders (Frequency)", min_value=1, max_value=100, value=5)
    hist_monetary = st.number_input("Total Historical Spend ($)", min_value=5.0, max_value=10000.0, value=450.0)
    avg_order_value = st.number_input("Avg Order Value ($)", min_value=5.0, max_value=2000.0, value=90.0)

    st.markdown("---")
    predict_btn = st.button("🚀 Predict & Generate Campaign", use_container_width=True, type="primary")

# 4. Main Dashboard Area
if predict_btn:
    with st.spinner("Analyzing CLV and prompting Campaign Agent..."):
        try:
            clv, tier, campaign_copy = get_agent_response(
                recency_days, frequency_orders, hist_monetary, avg_order_value
            )
            
            # Key Results Row
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="Predicted 90-Day CLV", value=f"${clv:.2f}")
                
            with col2:
                if tier == "VIP High Value":
                    st.success(f"**Segment:** {tier}")
                elif tier == "Mid-Tier Regular":
                    st.info(f"**Segment:** {tier}")
                else:
                    st.warning(f"**Segment:** {tier}")

            st.markdown("### ✉️ Recommended Campaign Strategy")
            
            # Display generated copy in a styled container
            with st.container(border=True):
                st.markdown(campaign_copy)
                
        except Exception as e:
            st.error(f"Error executing agent request: {str(e)}")
else:
    # Initial state placeholder
    st.info("👈 Adjust customer metrics in the sidebar and click **Predict & Generate Campaign** to view analysis.")
