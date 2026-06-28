package io.jenkins.plugins.chatbot;

import hudson.Extension;
import hudson.util.ListBoxModel;
import jenkins.model.GlobalConfiguration;
import com.cloudbees.plugins.credentials.common.StandardListBoxModel;
import com.cloudbees.plugins.credentials.domains.URIRequirementBuilder;
import org.jenkinsci.plugins.plaincredentials.StringCredentials;
import hudson.security.ACL;
import jenkins.model.Jenkins;
import org.kohsuke.stapler.DataBoundSetter;
import org.kohsuke.stapler.QueryParameter;
import org.jenkinsci.Symbol;

@Extension
@Symbol("chatbotConfig")
public class ChatbotGlobalConfig extends GlobalConfiguration {

    // Store the URL as a standard plain text string
    private String backendUrl;

    // Store only the ID of the jwtSecret, not the actual secret
    private String jwtSecretId;

    public ChatbotGlobalConfig() {
        // Load the saved configuration from disk on startup
        load();
    }

    public String getBackendUrl() {
        return backendUrl;
    }

    @DataBoundSetter
    public void setBackendUrl(String backendUrl) {
        this.backendUrl = backendUrl;
        save();
    }

    public String getJwtSecretId() {
        return jwtSecretId;
    }

    @DataBoundSetter
    public void setJwtSecretId(String jwtSecretId) {
        this.jwtSecretId = jwtSecretId;
        save();
    }

    // Automatically populates the dropdown menu in the Jenkins UI
    public ListBoxModel doFillJwtSecretIdItems(@QueryParameter String jwtSecretId) {
        if (!Jenkins.get().hasPermission(Jenkins.ADMINISTER)) {
            return new StandardListBoxModel().includeCurrentValue(jwtSecretId);
        }

        return new StandardListBoxModel()
                .includeEmptyValue()
                .includeMatchingAs(
                        ACL.SYSTEM2,
                        Jenkins.get(),
                        StringCredentials.class,
                        URIRequirementBuilder.create().build(),
                        null
                )
                .includeCurrentValue(jwtSecretId);
    }

    public static ChatbotGlobalConfig get() {
        return GlobalConfiguration.all().get(ChatbotGlobalConfig.class);
    }
}