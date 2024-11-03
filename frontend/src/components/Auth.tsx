import React, { useState } from "react";
import { signup, signin } from "../api/auth";

const Auth: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);

  const handleSubmit = async () => {
    if (isLogin) {
      await signin(username, password);
    } else {
      await signup(username, password);
      alert("User created successfully");
    }
  };

  return (
    <div>
      <h2>{isLogin ? "Login" : "Sign Up"}</h2>
      <input
        type="text"
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSubmit}>{isLogin ? "Login" : "Sign Up"}</button>
      <button onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? "Switch to Sign Up" : "Switch to Login"}
      </button>
    </div>
  );
};

export default Auth;
