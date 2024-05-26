import PhotoIcon from "@mui/icons-material/Photo";
import UploadFileRoundedIcon from "@mui/icons-material/UploadFileRounded";
import WallpaperIcon from "@mui/icons-material/Wallpaper";
import IosShareRoundedIcon from "@mui/icons-material/IosShareRounded";
import CreateIcon from "@mui/icons-material/Create";
import SaveAltIcon from "@mui/icons-material/SaveAlt";

// below is list of components that appear in sidebar
// id - unique id
// title - title of tool
// icon - imported icon from material ui
// component - component string needed for conditional rendering in itemsList.js
export const tools = [
  {
    id: 0,
    title: "Quotes",
    icon: <CreateIcon />,
    component: "textSection",
  },
  {
    id: 1,
    title: "Photos",
    icon: <PhotoIcon />,
    component: "imagesSection",
  },
  {
    id: 2,
    title: "Backgrounds",
    icon: <WallpaperIcon />,
    component: "backgroundsSection",
  },
  {
    id: 3,
    title: "Uploads",
    icon: <UploadFileRoundedIcon />,
    component: "uploadSection",
  },
  {
    id: 4,
    title: "Save",
    icon: <SaveAltIcon />,
    component: "saveSection",
  },
];
