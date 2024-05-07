import * as React from "react";
import { CssVarsProvider } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Sheet from "@mui/joy/Sheet";
import Layout from "./components/Layout";
import Navigation from "./components/Navigation";
import Header from "./components/Header";
import FileTable from "./components/FileTable/FileTable";
import Box from "@mui/joy/Box";
import { Button, Card } from "@mui/joy";
import { useState } from "react";
import axios from "axios";
import { API_URL } from "./constants";
export default function EteamApp() {
  return (
    <CssVarsProvider disableTransitionOnChange>
      <CssBaseline />
      <Layout.Root sx={{}}>
        <Layout.Header>
          <Header />
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
            <Sheet
              variant="outlined"
              sx={{
                margin: "auto",
                width: "50vw",
                borderRadius: "sm",
                display: { xs: "none", md: "flex" },
              }}
            >
              <FileTable />
            </Sheet>
            <TestFetch />
          </Box>
        </Layout.Main>
      </Layout.Root>
    </CssVarsProvider>
  );
}

function TestFetch() {
  const [message, setMessage] = useState([]);

  const onClick = () => {
    axios.get(API_URL + "/auth/hello").then((res) => {
      setMessage(res.data.hello);
    });
  };
  const replaceMessage = () => {
    setMessage(["dupa"]);
  };
  return (
    <div>
      <Button onClick={onClick} sx={{ padding: "24px" }}>
        fetch
      </Button>
      {message.map((item) => (
        <Card key={item} onClick={replaceMessage}>
          {item}
        </Card>
      ))}
    </div>
  );
}
