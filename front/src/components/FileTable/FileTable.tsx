import Table from "@mui/joy/Table";
import Typography from "@mui/joy/Typography";
import FileIcon from "@mui/icons-material/InsertDriveFile";
import FileDropdown from "./FileDropdown";
import * as React from "react";
import Box from "@mui/joy/Box";

export default function FileTable() {
  return (
    <div>
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
          <tr>
            <td>
              <Typography
                level="title-sm"
                startDecorator={<FileIcon color="primary" />}
                sx={{ alignItems: "flex-start" }}
              >
                test file
              </Typography>
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
                <Typography level="body-sm">123.3KB</Typography>
                <FileDropdown />
              </Box>
            </td>
          </tr>
        </tbody>
      </Table>
    </div>
  );
}
