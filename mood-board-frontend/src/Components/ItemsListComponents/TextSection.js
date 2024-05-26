import React from "react";
import items from "../../Data/items.json";

function TextSection(props) {
  const textsFilteredArray = items.filter(
    (el) => el.elementCategory === "texts"
  );

  return (
    <div className="itemsSection">
      <div className="itemsWrapper">
        {textsFilteredArray.map((item, i) => (
          <div className="imageContainer" key={i}>
            <img
              src={item.source}
              alt=""
              className="itemsImage"
              draggable="true"
              elementcategory={item.elementCategory}
              onDragStart={(e) => {
                props.onChangeDragUrl(e.target);
              }}
              onClick={(e) => {
                props.handleAddOnClick(e.target);
              }}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default TextSection;
