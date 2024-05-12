import { CssVarsProvider } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Layout from "./Layout";
import Header from "./Header";
import Navigation from "./Navigation";
import Box from "@mui/joy/Box";
import Sheet from "@mui/joy/Sheet";
import FileTable from "./FileTable/FileTable";
import * as React from "react";
import FileUpload from "./FileUpload";
import MainContent from "./MainContent";

function MainPage({ user, setUser }) {
  return (
    <CssVarsProvider disableTransitionOnChange>
      <CssBaseline />
      <Layout.Root sx={{}}>
        <Layout.Header>
          <Header
            user={user}
            onLogout={() => {
              sessionStorage.removeItem("user");
              setUser(null);
            }}
          />
        </Layout.Header>
        <Layout.SideNav>
          <Navigation />
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
            <MainContent />
          </Box>
        </Layout.Main>
      </Layout.Root>
    </CssVarsProvider>
  );
}
export default MainPage;
