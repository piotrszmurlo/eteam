import * as React from "react";
import { useState } from "react";
import MainPage from "./components/MainPage";
import LoginPage from "./components/Login/LoginPage";

export default function EteamApp() {
  const [user, setUser] = useState<any | null>(null);
  return (
    <div>
      {user != null ? (
        <MainPage user={user} setUser={setUser} />
      ) : (
        <LoginPage setUser={setUser} />
      )}
    </div>
  );
}
