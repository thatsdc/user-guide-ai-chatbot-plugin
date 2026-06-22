import { Box, TextField, IconButton } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import type { SubmitEventHandler } from "react";

export default function ChatInput({
  handleSendMessage,
  inputValue,
  setInputValue,
}: {
  handleSendMessage: SubmitEventHandler<HTMLFormElement>;
  inputValue: string;
  setInputValue: (s: string) => void;
}) {
  return (
    <Box
      component="form"
      onSubmit={handleSendMessage}
      sx={{
        p: 2,
        bgcolor: "background.paper",
        transition: (theme) => theme.transitions.create("background-color"),
      }}
    >
      <Box sx={{ display: "flex", gap: 1 }}>
        <TextField
          fullWidth
          size="small"
          value={inputValue}
          onChange={(event) => setInputValue(event.target.value)}
          placeholder="Write your message..."
          sx={{
            "& .MuiOutlinedInput-root": {
              borderRadius: 3, // rounded-xl
              bgcolor: (theme) =>
                theme.palette.mode === "light" ? "grey.50" : "grey.900",
            },
          }}
        />
        <IconButton
          type="submit"
          color="primary"
          sx={{
            bgcolor: "primary.main",
            color: "primary.contrastText",
            borderRadius: 3,
            "&:hover": {
              bgcolor: "primary.dark",
            },
          }}
          aria-label="Invia messaggio"
        >
          <SendIcon fontSize="small" />
        </IconButton>
      </Box>
    </Box>
  );
}
