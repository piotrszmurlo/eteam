import * as React from "react";
import { useEffect, useState } from "react";
import MainPage from "./components/MainPage";
import LoginPage from "./components/Login/LoginPage";

export default function EteamApp() {
  const [user, setUser] = useState<any | null>(null);

  useEffect(() => {
    try {
      const user = JSON.parse(sessionStorage.user);
      setUser(user);
    } catch (error) {}
  }, []);

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
