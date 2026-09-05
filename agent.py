import os
import joblib
import pandas as pd
from groq import Groq

model = joblib.load("clv_model.joblib")
scaler = joblib.load("scaler.joblib")
feature_names = joblib.load("feature_names.joblib")

def get_agent_response(recency_days, frequency_orders, hist_monetary, avg_order_value):
    input_df = pd.DataFrame([[recency_days, frequency_orders, hist_monetary, avg_order_value]], columns=feature_names)
    scaled_df = scaler.transform(input_df)
    predicted_clv = float(model.predict(scaled_df)[0])
    
    if predicted_clv >= 500:
        tier = "VIP High Value"
        angle = "Offer exclusive early access to new releases and a personal VIP discount."
    elif predicted_clv >= 150:
        tier = "Mid-Tier Regular"
        angle = "Provide a 15% discount incentive on their next order to boost purchase frequency."
    else:
        tier = "Low-Engagement / At-Risk"
        angle = "Provide a warm re-engagement win-back message with a special perk."

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
    You are an expert E-Commerce Marketing Copywriter & Behavioral Analyst.
    
    Customer Profile:
    - Recency: {recency_days} days ago
    - Frequency: {frequency_orders} orders
    - Total Spend: ${hist_monetary:.2f}
    - Avg Order Value: ${avg_order_value:.2f}
    - Predicted Future 90-Day CLV: ${predicted_clv:.2f}
    - Customer Segment: {tier}
    
    Strategy: {angle}
    
    Tasks:
    1. **Recommended Send-Time Window:** Recommend the best day and time to send this email based on customer recency and engagement tier, with a 1-sentence explanation.
    2. **Campaign Copy:** Write a compelling subject line and email body tailored to this segment.
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.4,
    )

    return predicted_clv, tier, response.choices[0].message.content