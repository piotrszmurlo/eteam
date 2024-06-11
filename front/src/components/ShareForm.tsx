import { Dialog, DialogContentText, TextField } from "@mui/material";
import { Button, DialogActions, DialogContent, DialogTitle } from "@mui/joy";
import * as React from "react";
import axios from "axios";
import { API_URL } from "../constants";

export default function ShareForm({ open, setOpen }) {
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <React.Fragment>
      <Dialog
        open={open}
        onClose={handleClose}
        PaperProps={{
          component: "form",
          onSubmit: (event: React.FormEvent<HTMLFormElement>) => {
            event.preventDefault();
            const formData = new FormData(event.currentTarget);
            const formJson = Object.fromEntries((formData as any).entries());
            const email = formJson.email;
            console.log(email);
            postShareFile(email);
            handleClose();
          },
        }}
      >
        <DialogTitle style={{ padding: "20px" }}>Share file</DialogTitle>
        <DialogContent style={{ padding: "20px" }}>
          <DialogContentText>
            To share file, provide user email.
          </DialogContentText>
          <TextField
            autoFocus
            required
            margin="dense"
            id="name"
            name="email"
            label="Email Address"
            // type="email"
            fullWidth
            variant="standard"
          />
        </DialogContent>
        <DialogActions style={{ padding: "20px" }}>
          <Button type="submit">Share</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}
const postShareFile = (user: string) => {
  const userId = JSON.parse(sessionStorage.user).sub;
  axios
    .post(
      API_URL + "/storage/shared_files",
      {
        user_id: user,
        owner_user_id: userId,
        file_id: "123",
      },
      {
        headers: {
          Authorization: "Bearer " + sessionStorage.id_token,
        },
      },
    )
    .then((res) => {})
    .catch((e) => {});
};
