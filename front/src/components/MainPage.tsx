import { CssVarsProvider } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Layout from "./Layout";
import Header from "./Header";
import Navigation from "./Navigation";
import Box from "@mui/joy/Box";
import * as React from "react";
import MainContent from "./MainContent";
import { useState } from "react";

function MainPage({ user, setUser }) {
  const [tab, setTab] = useState<string>("files");
  return (
    <CssVarsProvider disableTransitionOnChange>
      <CssBaseline />
      <Layout.Root sx={{}}>
        <Layout.Header>
          <Header
            user={user}
            onLogout={() => {
              sessionStorage.removeItem("user");
              sessionStorage.removeItem("id_token");
              setUser(null);
            }}
            onClickSettings={() => setTab("settings")}
          />
        </Layout.Header>
        <Layout.SideNav>
          <Navigation setTab={setTab} />
        </Layout.SideNav>
        <Layout.Main>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexDirection: "column",
            }}
          >
            <MainContent tab={tab} />
          </Box>
        </Layout.Main>
      </Layout.Root>
    </CssVarsProvider>
  );
}
export default MainPage;
