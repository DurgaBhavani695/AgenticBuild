import streamlit as st
import requests

class APIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    @property
    def token(self):
        return st.session_state.get("token")

    @token.setter
    def token(self, value):
        st.session_state.token = value

    def _get_headers(self):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, email, password):
        url = f"{self.base_url}/api/auth/login"
        try:
            response = requests.post(url, json={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                return True, "Login successful"
            else:
                try:
                    detail = response.json().get("detail", "Login failed")
                except:
                    detail = f"Login failed (Status {response.status_code})"
                return False, detail
        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def signup(self, email, password):
        url = f"{self.base_url}/api/auth/signup"
        try:
            response = requests.post(url, json={"email": email, "password": password})
            if response.status_code == 200:
                return True, "Signup successful. Please login."
            else:
                try:
                    detail = response.json().get("detail", "Signup failed")
                except:
                    detail = f"Signup failed (Status {response.status_code})"
                return False, detail
        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def _handle_response(self, response):
        if response.status_code == 401:
            # Clear token if unauthorized
            st.session_state.token = None
            st.rerun()
            
        if response.status_code == 200:
            return response.json()
        else:
            try:
                detail = response.json().get("detail", "Request failed")
            except:
                detail = f"Request failed (Status {response.status_code})"
            raise Exception(detail)

    def send_chat(self, query, mode, project_name=None, session_id=None):
        url = f"{self.base_url}/api/chat"
        payload = {
            "query": query,
            "mode": mode,
            "project_name": project_name,
            "session_id": session_id
        }
        response = requests.post(url, json=payload, headers=self._get_headers())
        return self._handle_response(response)

    def get_sessions(self):
        url = f"{self.base_url}/api/sessions"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            st.session_state.token = None
            st.rerun()
        return []

    def get_session_messages(self, session_id):
        url = f"{self.base_url}/api/sessions/{session_id}/messages"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            st.session_state.token = None
            st.rerun()
        return []

    def get_projects(self):
        url = f"{self.base_url}/api/projects"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            st.session_state.token = None
            st.rerun()
        return []

    def get_project_details(self, name):
        url = f"{self.base_url}/api/projects/{name}"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            st.session_state.token = None
            st.rerun()
        return None

    def get_download_url(self, name):
        return f"{self.base_url}/api/projects/{name}/download"

    def delete_project(self, name):
        url = f"{self.base_url}/api/projects/{name}"
        response = requests.delete(url, headers=self._get_headers())
        return response.status_code == 200

    def delete_session(self, session_id):
        url = f"{self.base_url}/api/sessions/{session_id}"
        response = requests.delete(url, headers=self._get_headers())
        return response.status_code == 200
