import { FileUploader } from "react-drag-drop-files";
import { useState } from "react";
import axios from "axios";
import { API_URL } from "../constants";
import { postUpgradePlan } from "./api";

function FileUpload({ onRefresh }) {
  const [file, setFile] = useState(null);
  const handleChange = (file) => {
    const form = new FormData();
    form.append("file_input", file);
    axios
      .post(API_URL + "/storage/files", form, {
        headers: {
          Authorization: "Bearer " + sessionStorage.id_token,
        },
      })
      .then((res) => {
        onRefresh();
      })
      .catch((error) => {
        if (error.response.status === 413) {
          postUpgradePlan("unlimited");
        }
      });
    setFile(file);
  };
  return <FileUploader handleChange={handleChange} name="file" />;
}

export default FileUpload;
