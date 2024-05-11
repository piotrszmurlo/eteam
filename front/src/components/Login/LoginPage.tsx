import { Card, CardContent } from "@mui/joy";
import Typography from "@mui/joy/Typography";
import GoogleSignInButton from "./GoogleSignInButton";
import * as React from "react";

function LoginPage({ setUser }) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        paddingTop: "25vh",
      }}
    >
      <LoginCard setUser={setUser} />
    </div>
  );
}

function LoginCard({ setUser }) {
  return (
    <Card
      color="primary"
      orientation="vertical"
      size="lg"
      variant="outlined"
      sx={{
        alignItems: "center",
      }}
    >
      <Typography level="title-lg" textColor="text.primary">
        ERSMS Storage Login
      </Typography>
      <CardContent orientation="horizontal" sx={{ paddingTop: "32px" }}>
        <GoogleSignInButton onSuccess={(email) => setUser(email)} />
      </CardContent>
    </Card>
  );
}

export default LoginPage;
