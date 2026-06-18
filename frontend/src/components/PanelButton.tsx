
export default function PanelButton({
  toggleChat,
  isOpen,
}: {
  toggleChat: () => void;
  isOpen: boolean;
}) {
  console.log(isOpen);

  return (
    !isOpen && (
      <button
        onClick={toggleChat}
        style={{
          position: "absolute",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          bottom: "20px",
          right: "20px",
          width: "60px",
          height: "60px",
          borderRadius: "50%",
          backgroundColor: "#000000",
          color: "white",
          border: "none",
          fontSize: "24px",
          cursor: "pointer",
          boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
        }}
      >
        {isOpen ? "⬇️" : "💬"}
      </button>
    )
  );
}
