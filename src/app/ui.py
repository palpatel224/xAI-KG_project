import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="KG-XAI Food Delivery", layout="wide")

st.title("KG-based XAI & Proactive Requirements Framework")

# Sidebar for Navigation
page = st.sidebar.selectbox("Choose a View", ["User View", "Admin Dashboard"])

if page == "User View":
    st.header("User Recommendation Demo")
    
    user_id = st.selectbox("Select User", ["u1", "u2", "u3"])
    
    if st.button("Get Recommendations"):
        try:
            response = requests.get(f"{API_URL}/recommend/{user_id}")
            if response.status_code == 200:
                recs = response.json()
                for rec in recs:
                    with st.expander(f"{rec['name']} ({rec['dish_id']})"):
                        st.write(f"**Explanation:** {rec['explanation']}")
            else:
                st.error("Failed to fetch recommendations")
        except requests.exceptions.ConnectionError:
            st.error("Is the backend running? (Run `python -m src.app.main`)")

elif page == "Admin Dashboard":
    st.header("Risk & Requirements Management")
    
    st.subheader("Report New Issue")
    col1, col2 = st.columns(2)
    
    with col1:
        issue_desc = st.text_input("Issue Description", "App crash on payment")
        st.markdown("**Vulnerability Scores (0-9)**")
        H = st.slider("Skill Level (H)", 0, 9, 5)
        Ro = st.slider("Reward (Ro)", 0, 9, 5)
        Ru = st.slider("Resources (Ru)", 0, 9, 5)
        D = st.slider("Ease of Discovery (D)", 0, 9, 5)
        E = st.slider("Ease of Exploitation (E)", 0, 9, 5)
        
    with col2:
        st.markdown("**Threat Scores (0-9)**")
        C = st.slider("Consequences (C)", 0, 9, 5)
        A = st.slider("Business Interruption (A)", 0, 9, 5)
        E_loss = st.slider("Economic Loss (E)", 0, 9, 5)
        R = st.slider("Reputation Loss (R)", 0, 9, 5)
        
    if st.button("Submit Issue"):
        payload = {
            "id": 101, # Random ID for demo
            "description": issue_desc,
            "vulnerability_scores": {"H": H, "Ro": Ro, "Ru": Ru, "D": D, "E": E},
            "threat_scores": {"C": C, "A": A, "E_loss": E_loss, "R": R}
        }
        try:
            res = requests.post(f"{API_URL}/issues", json=payload)
            if res.status_code == 200:
                st.success(f"Issue Reported! Severity: {res.json()['severity']}")
            else:
                st.error("Failed to report issue")
        except:
            st.error("Backend not reachable")

    st.divider()
    
    st.subheader("Current Risks & Requirements")
    if st.button("Refresh Data"):
        try:
            res = requests.get(f"{API_URL}/risks")
            if res.status_code == 200:
                data = res.json()
                
                st.write("### Issues Log")
                if data["issues"]:
                    st.dataframe(pd.DataFrame(data["issues"]))
                else:
                    st.info("No issues reported yet.")
                    
                st.write("### Proactive Requirements")
                for req in data["proactive_requirements"]:
                    st.warning(req)
                    
                st.write("### Forecasting Alerts")
                for alert in data["alerts"]:
                    st.error(alert)
        except:
            st.error("Backend not reachable")
