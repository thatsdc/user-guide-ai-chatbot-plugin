import PanelButton from "./components/PanelButton";
import SidePanel from "./components/SidePanel/SidePanel";
import { useEffect, useState } from "react";

const App = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [context, setContext] = useState<any>(null);

  useEffect(() => {
    if ((window as any).jenkinsAIContext) {
      setContext((window as any).jenkinsAIContext);
    }
  }, []);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  console.log(context);

  return (
    <div style={styles.container}>
      <SidePanel isOpen={isOpen} toggleChat={toggleChat} />
      <PanelButton isOpen={isOpen} toggleChat={toggleChat} />
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
