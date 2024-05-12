import { GoogleLogin } from "@react-oauth/google";
import axios from "axios";
import { API_URL } from "../../constants";

function GoogleSignInButton({ onSuccess }) {
  const errorMessage = (error) => {
    alert(error);
    console.log(error);
  };

  const login = (token: string) => {
    axios
      .post(API_URL + "/auth/token", { token: token })
      .then((res) => {
        onSuccess(res.data);
        console.log(res);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  return (
    <GoogleLogin
      onSuccess={(resp) => login(resp.credential)}
      onError={() => errorMessage}
    />
  );
}

export default GoogleSignInButton;
