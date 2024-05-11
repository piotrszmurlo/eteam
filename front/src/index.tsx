// @ts-ignore
import React from "react";
// @ts-ignore
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App.js";
import { GoogleOAuthProvider } from "@react-oauth/google";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <GoogleOAuthProvider clientId="941754735880-04vblvrihpsgk0glms6rb8djdtjerjiv.apps.googleusercontent.com">
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </GoogleOAuthProvider>,
);
