import PanelButton from "./components/PanelButton";
import SidePanel from "./components/SidePanel/SidePanel";
import { useState } from "react";
import { useColorMode } from "./theme/ThemeContext";

const App = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { mode, toggleColorMode } = useColorMode();

  const isDarkMode = mode === "dark";

  const handleToggleTheme = () => {
    toggleColorMode();
  };

  const togglePanel = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div style={styles.container}>
      <SidePanel
        isOpen={isOpen}
        toggleChat={togglePanel}
        isDarkMode={isDarkMode}
        onToggleDarkMode={handleToggleTheme}
      />
      <PanelButton isOpen={isOpen} toggleChat={togglePanel} />
    </div>
  );
};

const styles = {
  container: {
    zIndex: 99999,
    fontFamily: "sans-serif",
  },
};

export default App;
