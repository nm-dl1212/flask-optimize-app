import streamlit as st
import requests

# Set the backend URLs
user_url = "http://localhost:5001/user"
dummy_url = "http://localhost:5002/dummy"

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
st.title("User Management and Dummy Service Client")

# Check if user is signed in
if "access_token" in st.session_state:
    # Dummy Service Screen
    st.header("Dummy Service")
    x1 = st.number_input("Enter value for x1:", value=0.0)
    x2 = st.number_input("Enter value for x2:", value=0.0)

    # Button to send request to the /dummy endpoint
    if st.button("Send Request"):
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
        data = {"x1": x1, "x2": x2}
        
        try:
            response = requests.post(dummy_url, json=data, headers=headers)
            response_data = response.json()
            st.write("Message:", response_data.get("msg"))
            st.write("Calculated y value:", response_data.get("y"))
        except requests.exceptions.RequestException as e:
            st.error("Failed to connect to the backend.")

    # Log out button
    if st.button("Log Out"):
        st.session_state.pop("access_token", None)  # Reset the access token
        st.rerun()  # Reload the app to show the login screen

    if st.button("Delete User"):
        delete_response = delete_user(st.session_state["access_token"])
        st.write(delete_response)
        st.session_state.pop("access_token", None)  # reset access token
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