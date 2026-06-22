import { Box, Typography } from "@mui/material";
import type { ChatMessage } from "../../../../types/types";
import EditInput from "./EditInput";
import { useState } from "react";
import MessageActions from "./MessageActions";

interface MessageProps {
  message: ChatMessage;
  onRetry: (message: ChatMessage) => void;
  onEditConfirm: (message: ChatMessage, newText: string) => void;
}

function formatTime(isoString: string) {
  return new Date(isoString).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function Message({
  message,
  onRetry,
  onEditConfirm,
}: MessageProps) {
  const isUser = message.sender === "user";
  const [copied, setCopied] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(message.text);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const handleStartEdit = () => {
    setEditValue(message.text);
    setIsEditing(true);
  };

  const handleCancelEdit = () => {
    setEditValue(message.text);
    setIsEditing(false);
  };

  const handleConfirmEdit = () => {
    const trimmed = editValue.trim();
    if (!trimmed) return;
    onEditConfirm(message, trimmed);
    setIsEditing(false);
  };

  return (
    <Box
      className="message-row"
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: isUser ? "flex-end" : "flex-start",
      }}
    >
      {isEditing ? (
        <EditInput
          editValue={editValue}
          handleCancelEdit={handleCancelEdit}
          handleConfirmEdit={handleConfirmEdit}
          setEditValue={setEditValue}
        />
      ) : (
        <Box
          sx={(theme) => ({
            maxWidth: "80%",
            minWidth: 0,
            px: 2,
            py: 1.25,
            fontSize: "0.875rem",
            boxShadow: theme.shadows[1],
            transition: theme.transitions.create(["background-color", "color"]),
            borderRadius: 2,
            wordBreak: "break-word",
            overflowWrap: "break-word",
            whiteSpace: "pre-wrap",
            ...(isUser
              ? {
                  bgcolor: "primary.main",
                  color: "primary.contrastText",
                  borderTopRightRadius: 0,
                }
              : {
                  bgcolor: "background.paper",
                  color: "text.primary",
                  border: `1px solid ${theme.palette.divider}`,
                  borderTopLeftRadius: 0,
                }),
          })}
        >
          {message.text}
        </Box>
      )}

      {!isEditing && (
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 0.5,
            mt: 0.5,
            px: 0.5,
            flexDirection: isUser ? "row-reverse" : "row",
          }}
        >
          <Typography
            variant="caption"
            sx={{ color: "text.disabled", fontWeight: 300, userSelect: "none" }}
          >
            {formatTime(message.createdAt)}
          </Typography>

          <MessageActions
            copied={copied}
            handleCopy={handleCopy}
            handleStartEdit={handleStartEdit}
            isUser={isUser}
            onRetry={() => onRetry(message)}
          />
        </Box>
      )}
    </Box>
  );
}
