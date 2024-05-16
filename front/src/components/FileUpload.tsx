import { FileUploader } from "react-drag-drop-files";
import { useState } from "react";
import axios from "axios";
import { API_URL } from "../constants";

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
          console.log(error.response.data);
          axios
            .post(
              API_URL + "/payment/create_payment",
              {
                upgrade_plan_name: "unlimited",
              },
              {
                headers: {
                  Authorization: "Bearer " + sessionStorage.id_token,
                },
              },
            )
            .then((res) => {
              window.location.replace(res.data.payment_url);
            })
            .catch((e) => {});
        }
      });
    setFile(file);
  };
  return <FileUploader handleChange={handleChange} name="file" />;
}

export default FileUpload;
