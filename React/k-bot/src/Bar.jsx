const MenuBar = (props) => {
  var typeName = props.typeName || "BottomBar";

  return (
    <div className={`acrylic ${typeName}`} id="menu-bar">
      <h1>Tap to start...</h1>
    </div>
  );
};

export default MenuBar;
