import streamlit as st
import requests
import json
import time
import os
import plotly.graph_objects as go

# Set the backend URLs
user_url = os.environ["USER_URL"]  # "http://localhost:5001/user"
dummy_url = os.environ["DUMMY_URL"]  # "http://localhost:5002/dummy"
optimize_url = os.environ["OPTIMIZE_URL"]  # "http://localhost:5003/optimize"


# Function to sign up a new user
def signup(username, password):
    response = requests.post(
        f"{user_url}/signup", json={"username": username, "password": password}
    )
    return response.json()


# Function to sign in and get JWT token
def signin(username, password):
    response = requests.post(
        f"{user_url}/signin", json={"username": username, "password": password}
    )
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
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# Check if user is signed in
if st.session_state["access_token"]:

    tab1, tab2, tab3 = st.tabs(["Dummy", "Optimization", "UserSetting"])

    with tab1:
        st.write("input: ")
        x1 = st.number_input("x1:", value=0.0)
        x2 = st.number_input("x2:", value=0.0)

        # Button to send request to the /dummy endpoint
        if st.button("Calculate"):
            headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
            data = {"x1": x1, "x2": x2}

            try:
                # ダミーAPIにリクエスト
                response = requests.post(dummy_url, json=data, headers=headers)
                if response.status_code == 200:
                    response_data = response.json()
                    st.write("Calculated y value:", response_data.get("y"))
                    st.success(response_data.get("msg"), icon="✅")

                else:
                    response_data = response.json()
                    st.error(
                        f'ERROR code:{response.status_code}  msg:{response_data.get("msg")}',
                        icon="🔥",
                    )

            except requests.exceptions.RequestException as e:
                st.error("Failed to connect to the dummy server", icon="📡⚡️")

    with tab2:
        st.write("input: ")
        max_iteration = st.number_input("max_iteration:", value=10)

        if st.button("Optimize run"):
            headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
            data = {"max_iteration": max_iteration}

            with st.status("Running...", expanded=False) as status:

                try:
                    # 最適化APIにリクエスト
                    response = requests.post(
                        optimize_url, json=data, headers=headers, stream=True
                    )

                    if response.status_code == 200:
                        response_placeholder = st.empty()

                        data_n = []
                        data_y = []
                        fig = go.Figure()
                        fig.add_trace(
                            go.Scatter(
                                x=data_n,
                                y=data_y,
                                mode="lines+markers",
                                name="リアルタイムデータ",
                            )
                        )
                        plot_placeholder = st.plotly_chart(
                            fig, use_container_width=True
                        )

                        for line in response.iter_lines():
                            if line:
                                decoded_line = line.decode("utf-8")
                                response_data = json.loads(decoded_line)
                                with response_placeholder.container():
                                    st.write(response_data)

                                    # グラフに追加していく
                                    new_n = response_data.get("latest").get("number")
                                    new_y = response_data.get("latest").get("value")
                                    data_n.append(new_n)
                                    data_y.append(new_y)

                                    # グラフに埋め込む
                                    fig.data[0].x = data_n
                                    fig.data[0].y = data_y
                                    plot_placeholder.plotly_chart(
                                        fig, use_container_width=True
                                    )

                        st.success("Optimizaion complete", icon="✅")

                    else:
                        response_data = response.json()
                        st.error(
                            f'ERROR  code:{response.status_code}  msg:{response_data.get("msg")}',
                            icon="🔥",
                        )

                except requests.exceptions.RequestException as e:
                    st.error("Failed to connect to the optimize server", icon="📡⚡️")

                status.update(label="Complete!!!", state="complete", expanded=True)

    with tab3:
        # Log out button
        if st.button("Log Out"):
            st.session_state["access_token"] = None
            st.rerun()  # Reload the app to show the login screen

        if st.button("Delete User"):
            response = delete_user(st.session_state["access_token"])
            if response == 200:
                st.success(response, icon="✅")
                st.session_state["access_token"] = None
                st.rerun()  # Reload the app to show the login screen
            else:
                st.error(
                    f'ERROR  code:{response.status_code}  msg:{response_data.get("msg")}',
                    icon="🔥",
                )

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
