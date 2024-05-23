import * as React from "react";
import UpgradePlan from "./UpgradePlan";
import FilesPage from "./FilePage";
import UpgradePlanCards from "./UpgradePlan";

function MainContent({ tab, openDialog }) {
  if (tab == "settings") return <UpgradePlanCards />;
  return <FilesPage openDialog={openDialog} />;
}

export default MainContent;
