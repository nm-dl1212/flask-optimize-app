import streamlit as st
import requests
import json
import time

# Set the backend URLs
user_url = "http://localhost:5001/user"
dummy_url = "http://localhost:5002/dummy"
optimize_url = "http://localhost:5003/optimize"

# Function to sign up a new user
def signup(username, password):
    response = requests.post(f"{user_url}/signup", json={"username": username, "password": password})
    return response.json()

# Function to sign in and get JWT token
def signin(username, password):
    response = requests.post(f"{user_url}/signin", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

# Function to delete the user
def delete_user(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(f"{user_url}/delete_user", headers=headers)
    return response.json()

# -------------------------

# Streamlit app title
st.title("Optimize Service Client")

# initialize session_state for token
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None

# Check if user is signed in
if st.session_state['access_token']:

    tab1, tab2, tab3 = st.tabs(["Dummy", "Optimization", "UserSetting"])

    with tab1:
        x1 = st.number_input("Enter value for x1:", value=0.0, )
        x2 = st.number_input("Enter value for x2:", value=0.0)

        # Button to send request to the /dummy endpoint
        if st.button("Send Request"):
            headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
            data = {"x1": x1, "x2": x2}
            
            try:
                response = requests.post(dummy_url, json=data, headers=headers)
                response_data = response.json()
                st.write("Calculated y value:", response_data.get("y"))
                st.success(response_data.get("msg"), icon="✅")
            except requests.exceptions.RequestException as e:
                st.error("Failed to connect to the dummy server", icon="🔥")

    with tab2:
        # Button to send request to the /optimize endpoint
        if st.button("Optimize run"):
            headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
            
            with st.status("Optimize running...", expanded=False) as status:
                
                try:
                    response = requests.post(optimize_url, headers=headers, stream=True)

                    if response.status_code == 200:
                        res_space = st.empty()
                        for line in response.iter_lines():
                            decoded_line = line.decode('utf-8')
                            response_data = json.loads(decoded_line)
                            with res_space.container():
                                st.write(response_data)
                        
                        st.success(response_data.get("msg"), icon="✅")
                    else:
                        st.error("Failed to start optimization", icon="🔥")

                except requests.exceptions.RequestException as e:
                    st.error("Failed to connect to the optimize server", icon="🔥")

                status.update(
                    label="Optimize complete!", state="complete", expanded=True
                )

    with tab3:
        # Log out button
        if st.button("Log Out"):
            st.session_state['access_token'] = None
            st.rerun()  # Reload the app to show the login screen

        if st.button("Delete User"):
            delete_response = delete_user(st.session_state["access_token"])
            st.write(delete_response)
            st.session_state['access_token'] = None
            st.rerun()  # Reload the app to show the login screen
            
else:
    # Login Screen with Tabs
    tab1, tab2 = st.tabs(["Sign Up", "Sign In"])

    with tab1:
        st.subheader("Sign Up")
        signup_username = st.text_input("Username")
        signup_password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            signup_response = signup(signup_username, signup_password)
            st.write(signup_response)

    with tab2:
        st.subheader("Sign In")
        signin_username = st.text_input("Username", key="signin")
        signin_password = st.text_input("Password", type="password", key="signin_pass")
        if st.button("Sign In"):
            access_token = signin(signin_username, signin_password)
            if access_token:
                st.session_state["access_token"] = access_token
                st.success("Signed in successfully!")
                st.rerun()  # Reload the app to show the dummy service screen
            else:
                st.error("Failed to sign in.")