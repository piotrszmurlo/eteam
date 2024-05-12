import Table from "@mui/joy/Table";
import Typography from "@mui/joy/Typography";
import FileIcon from "@mui/icons-material/InsertDriveFile";
import FileDropdown from "./FileDropdown";
import * as React from "react";
import Box from "@mui/joy/Box";
import axios from "axios";
import { API_URL } from "../../constants";
import { useState } from "react";
import { ButtonGroup, Input } from "@mui/joy";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import IconButton from "@mui/joy/IconButton";

export default function FileTable({ files, refreshFiles }) {
  return (
    <Table
      size="lg"
      borderAxis="none"
      variant="soft"
      sx={{
        "--TableCell-paddingX": "1rem",
        "--TableCell-paddingY": "1rem",
      }}
    >
      <thead>
        <tr>
          <th>
            <Typography level="title-sm">File</Typography>
          </th>
          <th>
            <Typography level="title-sm">Last modified</Typography>
          </th>
          <th>
            <Typography level="title-sm">Size</Typography>
          </th>
        </tr>
      </thead>
      <tbody>
        {files.map((file) => {
          return <FileRow key={file.id} file={file} onRefresh={refreshFiles} />;
        })}
      </tbody>
    </Table>
  );
}

function FileRow({ key, file, onRefresh }) {
  const [newFileName, setNewFilename] = useState<string>(file.file_name);
  const [isRenaming, setIsRenaming] = useState<boolean>(false);

  const deleteFile = () => {
    axios
      .delete(API_URL + "/storage/files", {
        params: {
          file_id: file.file_id,
        },
        headers: {
          Authorization: "Bearer " + sessionStorage.id_token,
        },
      })
      .then((res) => onRefresh())
      .catch(() => alert("failed to delete"));
  };

  return (
    <tr key={key}>
      <td>
        {isRenaming ? (
          <form
            onSubmit={(event) => {
              event.preventDefault();
              axios
                .patch(
                  API_URL + "/storage/files",
                  {
                    file_name: newFileName,
                  },
                  {
                    params: {
                      file_id: file.file_id,
                    },
                    headers: {
                      Authorization: "Bearer " + sessionStorage.id_token,
                    },
                  },
                )
                .then(() => {
                  setIsRenaming(false);
                  onRefresh();
                })
                .catch(() => alert("rename error"));
            }}
          >
            <Box style={{ flexDirection: "row", display: "flex" }}>
              <Input
                type="text"
                required
                startDecorator={<FileIcon color="primary" />}
                placeholder="New file name..."
                value={newFileName}
                onChange={(e) => setNewFilename(e.target.value)}
              />
              <ButtonGroup>
                <IconButton type="submit">
                  <CheckIcon />
                </IconButton>
                <IconButton
                  onClick={() => {
                    setIsRenaming(false);
                  }}
                >
                  <CloseIcon />
                </IconButton>
              </ButtonGroup>
            </Box>
          </form>
        ) : (
          <Typography
            level="title-sm"
            startDecorator={<FileIcon color="primary" />}
            sx={{ alignItems: "flex-start" }}
          >
            {file.file_name}
          </Typography>
        )}
      </td>
      <td>
        <Typography level="body-sm">14 Mar 2021, 7PM</Typography>
      </td>
      <td>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexDirection: "row",
          }}
        >
          <Typography level="body-sm">{file.file_size}MB</Typography>
          <FileDropdown
            onStartRename={() => setIsRenaming(true)}
            onDelete={deleteFile}
          />
        </Box>
      </td>
    </tr>
  );
}
