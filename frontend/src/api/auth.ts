import axios from "axios";

export const signup = async (username: string, password: string) => {
  console.log("signup request");
  return axios.post(`user/signup`, { username, password });
};

export const signin = async (username: string, password: string) => {
  console.log("signin request");
  const response = await axios.post(`user/signin`, { username, password });
  const token = response.data.access_token;
  localStorage.setItem("token", token);
  return token;
};
