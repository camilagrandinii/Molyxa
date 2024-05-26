import React from "react";
import DownloadRoundedIcon from "@mui/icons-material/DownloadRounded";

function SaveSection(props) {
  const handleExport = () => {
    const uri = props.stageRef.current.toDataURL();
    const link = document.createElement("a");
    link.download = "moodboard-export.png";
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleSave = async () => {
    try {
      const itemsWithoutId = props.images.map(({ id, ...rest }) => rest);

      const answer = await fetch("http://localhost:5000/api/mood-board", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: "Moodboard", items: itemsWithoutId }),
      });

      if (answer.ok) {
        console.log("Moodboard state saved successfully!");
      } else {
        console.error("Error saving moodboard state:", answer.status);
      }
    } catch (error) {
      console.error("Error sending request:", error);
    }
  };

  return (
    <div className="itemsSection">
      <div className="saveSectionWrap">
        <button onClick={handleSave} className="downloadImage">
          <DownloadRoundedIcon />
          Save MoodBoard State
        </button>
        <button onClick={handleExport} className="downloadImage">
          <DownloadRoundedIcon />
          Export canvas as image
        </button>
      </div>
    </div>
  );
}

export default SaveSection;
