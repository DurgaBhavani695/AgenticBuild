import streamlit as st
import re
from frontend.utils.api_client import APIClient

def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

def is_valid_password(password):
    # Requirement: Min 8 chars, at least one letter and one number
    return len(password) >= 8 and any(c.isalpha() for c in password) and any(c.isdigit() for c in password)

def render_auth_page():
    st.title("🔐 AgenticBuild Auth")
    
    api_client = APIClient()
    
    auth_mode = st.radio("Choose Action:", ["Login", "Sign Up"], horizontal=True)
    
    if auth_mode == "Sign Up":
        st.info("💡 **Password Requirements:**\n- Minimum 8 characters\n- At least one letter and one number")

    with st.form("auth_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button(auth_mode)
        
        if submit:
            if not email or not password:
                st.error("Please fill in all fields.")
            elif auth_mode == "Sign Up":
                if not is_valid_email(email):
                    st.error("Please enter a valid email address.")
                elif not is_valid_password(password):
                    st.error("Password must be at least 8 characters long and contain both letters and numbers.")
                else:
                    success, message = api_client.signup(email, password)
                    if success:
                        st.success("Account created and logged in successfully!")
                        st.rerun()
                    else:
                        st.error(message)
            else:
                # Login mode
                success, message = api_client.login(email, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
