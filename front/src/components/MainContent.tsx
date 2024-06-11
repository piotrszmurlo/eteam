import * as React from "react";
import UpgradePlan from "./UpgradePlan";
import FilesPage from "./FilePage";
import UpgradePlanCards from "./UpgradePlan";
import SharedFilesPage from "./SharedFilePage";

function MainContent({ tab, openDialog }) {
  if (tab == "settings") return <UpgradePlanCards />;
  if (tab == "shared") return <SharedFilesPage openDialog={openDialog} />;
  return <FilesPage openDialog={openDialog} />;
}

export default MainContent;
