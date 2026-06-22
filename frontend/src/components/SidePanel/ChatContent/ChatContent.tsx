import { Stack } from "@mui/material";
import type { ChatMessage } from "../../../types/types";
import Message from "./Message/Message";
import { customScrollbar } from "../../../theme/scrollBarStyles";
import TypingIndicator from "./TypingIndicator";

export default function ChatContent({
  messages,
  isBotTyping,
  onEditMessageConfirm,
  onRetryMessage,
}: {
  messages: ChatMessage[];
  isBotTyping: boolean;
  onEditMessageConfirm: (m: ChatMessage, newText: string) => void;
  onRetryMessage: (m: ChatMessage) => void;
}) {
  const onEditConfirm = (message: ChatMessage, newText: string) => {
    onEditMessageConfirm(message, newText);
  };
  const onRetry = (message: ChatMessage) => {
    onRetryMessage(message);
  };

  return (
    <Stack
      spacing={2}
      sx={(theme) => ({
        flex: 1,
        overflowY: "auto",
        scrollbarGutter: "stable",
        p: 2,
        transition: theme.transitions.create("background-color"),
        ...customScrollbar(theme),
      })}
    >
      {messages.map((m) => (
        <Message
          key={m.id}
          message={m}
          onEditConfirm={onEditConfirm}
          onRetry={onRetry}
        />
      ))}
      {isBotTyping && <TypingIndicator />}
    </Stack>
  );
}
