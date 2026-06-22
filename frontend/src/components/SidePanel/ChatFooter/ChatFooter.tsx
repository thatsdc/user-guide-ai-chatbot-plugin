import React, { type SubmitEventHandler } from "react";
import ChatInput from "./ChatInput";
import { ChatTools } from "./ChatTools";

export default function ChatFooter({
  handleSendMessage,
  inputValue,
  setInputValue,
}: {
  handleSendMessage: SubmitEventHandler<HTMLFormElement>;
  inputValue: string;
  setInputValue: (s: string) => void;
}) {
  const onAttachContext = () => {};

  return (
    <div>
      <ChatTools onAttachContext={onAttachContext} currentPageName="Sample" />
      <ChatInput
        handleSendMessage={handleSendMessage}
        inputValue={inputValue}
        setInputValue={setInputValue}
      />
    </div>
  );
}
