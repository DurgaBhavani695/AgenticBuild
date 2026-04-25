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
                # On successful signup, immediately log the user in
                return self.login(email, password)
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

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self._get_headers(), **kwargs)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            st.error("🔌 **Backend Offline**: Could not connect to the AgenticBuild server. Please ensure the backend is running (port 8000).")
            st.stop()
        except Exception as e:
            raise e

    def send_chat(self, query, mode, project_name=None, session_id=None, model_name=None):
        payload = {
            "query": query,
            "mode": mode,
            "project_name": project_name,
            "session_id": session_id,
            "model_name": model_name
        }
        return self._make_request("POST", "/api/chat", json=payload)

    def get_sessions(self):
        try:
            return self._make_request("GET", "/api/sessions")
        except:
            return []

    def get_session_messages(self, session_id):
        try:
            return self._make_request("GET", f"/api/sessions/{session_id}/messages")
        except:
            return []

    def get_projects(self):
        try:
            return self._make_request("GET", "/api/projects")
        except:
            return []

    def get_project_details(self, name):
        try:
            return self._make_request("GET", f"/api/projects/{name}")
        except:
            return None

    def get_download_url(self, name):
        return f"{self.base_url}/api/projects/{name}/download"

    def delete_project(self, name):
        try:
            self._make_request("DELETE", f"/api/projects/{name}")
            return True
        except:
            return False

    def delete_session(self, session_id):
        try:
            self._make_request("DELETE", f"/api/sessions/{session_id}")
            return True
        except:
            return False
