import axios from "axios";
import { PAYMENT_URL } from "../constants";

const postUpgradePlan = (planName: string) => {
  axios
    .post(
      PAYMENT_URL + "/create_payment",
      {
        upgrade_plan_name: planName,
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
};

export { postUpgradePlan };
