package io.jenkins.plugins.chatbot;

import hudson.Extension;
import hudson.model.RootAction;


@Extension
public class ChatbotApiAction implements RootAction {

    final private String BASE_URL = "chatbot-api";

    @Override
    public String getIconFileName() {
        return null; 
    }

    @Override
    public String getDisplayName() {
        return null;
    }

    @Override
    public String getUrlName() {
        return BASE_URL;
    }
}