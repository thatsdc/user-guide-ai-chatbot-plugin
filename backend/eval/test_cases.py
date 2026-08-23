import json

ANSWER_RELEVANCY_TEST_CASES = [
    # ==========================================
    # BASIC QUERIES (5 Test Cases)
    # ==========================================
    {
        # Test Case 1: Simple build status check
        "question": "Did my last build succeed and how long did it take?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {
                        "number": 13,
                        "result": "SUCCESS",
                        "duration": 5821,
                        "timestamp": 1785750805237,
                        "causes": ["Started by user anonymous"],
                    },
                    "build_logs": "Finished: SUCCESS",
                }
            )
        },
    },
    {
        # Test Case 2: Master node hardware/OS information
        "question": "How much free memory does the Jenkins master node have, and what OS is it running?",
        "dummy_context": {
            "get_general_jenkins_context": json.dumps(
                {
                    "master_node": {
                        "executors": 2,
                        "is_online": True,
                        "system_info": {
                            "os_name": "Windows 11",
                            "java_version": "21.0.10",
                            "free_memory_mb": 186,
                            "total_memory_mb": 512,
                        },
                    }
                }
            )
        },
    },
    {
        # Test Case 3: Installed plugin version check
        "question": "What version of the git plugin is currently installed?",
        "dummy_context": {
            "get_installed_plugin_list": json.dumps(
                {
                    "git-client": "6.6.1",
                    "git": "5.10.1",
                    "credentials": "1496.vf6821f162d4e",
                }
            )
        },
    },
    {
        # Test Case 4: Out of Scope query
        "question": "Can you give me a recipe for chocolate chip cookies?",
        "dummy_context": {
            "get_general_jenkins_context": json.dumps({"jenkins_version": "2.528.3"})
        },
    },
    {
        # Test Case 5: Current UI screen
        "question": "What Jenkins screen am I currently looking at?",
        "dummy_context": {
            "get_general_jenkins_context": json.dumps(
                {
                    "current_screen": "Build Job Pipeline",
                    "root_url": "http://localhost:8080/jenkins/",
                    "jenkins_version": "2.528.3",
                }
            )
        },
    },
    # ==========================================
    # TROUBLESHOOTING & PROBLEM SOLVING (10 Test Cases)
    # ==========================================
    {
        # Test Case 6: NPM script missing (Requires Tree -> File + Logs)
        "question": "My build failed with 'npm ERR! missing script: build'. Can you check my build logs and then look at my package.json to see what scripts are actually defined?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 45, "status": "FAILURE"},
                    "build_logs": "npm ERR! missing script: build\nnpm ERR! A complete log of this run can be found in...\nFinished: FAILURE",
                }
            ),
            "get_workspace_tree": "=== Workspace ID: 21 ===\n- src/main.js\n- package.json",
            "get_workspace_file": json.dumps(
                {
                    "name": "my-app",
                    "scripts": {
                        "start": "node index.js",
                        "test": "jest",
                        # 'build' script is clearly missing here
                    },
                }
            ),
        },
    },
    {
        # Test Case 7: Syntax Error in Jenkinsfile (Requires Tree -> File + Logs)
        "question": "The build failed with a syntax error in the Jenkinsfile. Can you inspect the Jenkinsfile in the workspace and tell me which line has the issue?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 88, "status": "FAILURE"},
                    "build_logs": "WorkflowScript: 5: Expected a step @ line 5, column 9.\n           sh 'npm run test'\n           ^\n\n1 error\nFinished: FAILURE",
                }
            ),
            "get_workspace_tree": "=== Workspace ID: default ===\n- src/\n- Jenkinsfile",
            "get_workspace_file": "pipeline {\n  agent any\n  stages {\n    stage('Test') {\n      sh 'npm run test' // Missing 'steps' block wrapping this command\n    }\n  }\n}",
        },
    },
    {
        # Test Case 8: Missing Artifacts Directory Mismatch (Requires Tree + Logs)
        "question": "My build says it succeeded, but the 'archiveArtifacts' step failed to find 'target/app.jar'. Can you check the workspace tree to see if the file was generated in a different folder?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 102, "status": "FAILURE"},
                    "build_logs": 'Archiving artifacts\nERROR: No artifacts found that match the file pattern "target/app.jar". Configuration error?\nFinished: FAILURE',
                }
            ),
            "get_workspace_tree": "=== Workspace ID: 15 ===\n- build/app.jar\n- src/\n- pom.xml",
            # The artifact is in 'build/' instead of 'target/'
        },
    },
    {
        # Test Case 9: Missing Plugin DSL Method (Requires Job Details + Plugin List)
        "question": "My pipeline fails saying 'No such DSL method podTemplate'. Can you check my job configuration and verify if the Kubernetes plugin is actually installed?",
        "dummy_context": {
            "get_job_details": json.dumps(
                {
                    "config_xml": 'pipeline {\n  agent {\n    kubernetes {\n      yaml """\n        apiVersion: v1\n        kind: Pod\n      """\n    }\n  }\n  stages {}\n}'
                }
            ),
            "get_installed_plugin_list": json.dumps(
                {
                    "git": "5.10.1",
                    "workflow-aggregator": "608.v67378e9d3db_1",
                    # Kubernetes plugin is missing from this list
                }
            ),
        },
    },
    {
        # Test Case 10: Out of Memory Error (Requires Logs + VectorDB Docs)
        "question": "The pipeline crashed suddenly. Find the exact error in the logs and tell me how to fix it based on the official Jenkins documentation.",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 33, "status": "FAILURE"},
                    "build_logs": "java.lang.OutOfMemoryError: Java heap space\n at org.apache.maven.lifecycle.internal.BuilderCommon\nFinished: FAILURE",
                }
            ),
            "fetch_from_vectordb": "DOCUMENT 0:\nTroubleshooting OutOfMemoryError in Jenkins Builds\nIf a Maven build fails with java.lang.OutOfMemoryError: Java heap space, you must increase the memory available to the Maven process. This is done by setting the MAVEN_OPTS environment variable, for example: env.MAVEN_OPTS = '-Xmx1024m'.",
        },
    },
    {
        # Test Case 11: Script Security Sandbox Rejection (Requires Logs + VectorDB)
        "question": "The pipeline aborted with 'RejectedAccessException'. What caused this and how do I fix it?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 12, "status": "FAILURE"},
                    "build_logs": "org.jenkinsci.plugins.scriptsecurity.sandbox.RejectedAccessException: Scripts not permitted to use new java.io.File java.lang.String\nFinished: FAILURE",
                }
            ),
            "fetch_from_vectordb": "DOCUMENT 0:\nScript Security and In-process Script Approval\nWhen a pipeline runs in the Groovy sandbox, certain sensitive Java methods (like java.io.File) are blocked by default resulting in a RejectedAccessException. An administrator must go to 'Manage Jenkins' -> 'In-process Script Approval' to manually permit the method.",
        },
    },
    {
        # Test Case 12: Docker Agent Configuration Error (Requires Tree -> File + Logs)
        "question": "My declarative pipeline fails immediately when trying to spin up the Docker agent. Look at the logs and my Jenkinsfile to explain what I configured wrong.",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 5, "status": "FAILURE"},
                    "build_logs": "java.io.IOException: Failed to run image 'maven:3-alpine'. Error: docker: command not found.\nFinished: FAILURE",
                }
            ),
            "get_workspace_tree": "=== Workspace ID: 8 ===\n- src/\n- Jenkinsfile",
            "get_workspace_file": "pipeline {\n  agent {\n    docker {\n      image 'maven:3-alpine'\n    }\n  }\n  stages {\n    stage('Build') { steps { sh 'mvn clean install' } }\n  }\n}",
            # The issue is that the underlying Jenkins node doesn't have Docker installed (docker: command not found)
        },
    },
    {
        # Test Case 13: Stuck in Queue due to Offline Node (Requires General Context)
        "question": "Why is my build stuck in the queue for 2 hours? Is the master node offline or out of executors?",
        "dummy_context": {
            "get_general_jenkins_context": json.dumps(
                {
                    "master_node": {
                        "executors": 0,
                        "is_online": False,
                        "system_message": "Node is currently undergoing maintenance.",
                    }
                }
            )
        },
    },
    {
        # Test Case 14: Webhook not triggering (Requires Job Details)
        "question": "GitHub webhooks stopped triggering this job. Check the job configuration to see if the GitHub hook trigger is actually enabled.",
        "dummy_context": {
            "get_job_details": json.dumps(
                {
                    "config_xml": "<?xml version='1.1' encoding='UTF-8'?>\n<flow-definition>\n  <triggers/> <!-- Triggers block is completely empty, GitHubPushTrigger is missing -->\n  <disabled>false</disabled>\n</flow-definition>"
                }
            )
        },
    },
    {
        # Test Case 15: Pipeline Timeout (Requires Logs + Tree -> File)
        "question": "The build was aborted due to a timeout. Can you check the logs to see where it got stuck, and then check the Jenkinsfile to see what the timeout limit was set to?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 99, "status": "ABORTED"},
                    "build_logs": "[Pipeline] sh\n+ npm run e2e-tests\nStarting end-to-end tests...\nCancelling nested steps due to timeout\nBody did not finish within grace period; terminating with extreme prejudice\nFinished: ABORTED",
                }
            ),
            "get_workspace_tree": "=== Workspace ID: 44 ===\n- tests/\n- Jenkinsfile",
            "get_workspace_file": "pipeline {\n  agent any\n  options {\n    timeout(time: 5, unit: 'MINUTES') // Timeout is too short for e2e tests\n  }\n  stages {\n    stage('E2E') {\n      steps {\n        sh 'npm run e2e-tests'\n      }\n    }\n  }\n}",
        },
    },
]

FAITHFULNESS_TEST_CASES = [
    # ==========================================
    # DIRECT EXTRACTION (The agent must strictly use provided facts)
    # ==========================================
    {
        # Test Case 1: Simple fact extraction
        "question": "What is the current Jenkins version?",
        "dummy_context": {
            "get_general_jenkins_context": json.dumps({"jenkins_version": "2.440.1"})
        },
    },
    {
        # Test Case 2: Exact plugin version extraction
        "question": "Which version of the workflow-cps plugin is installed?",
        "dummy_context": {
            "get_installed_plugin_list": json.dumps(
                {"workflow-cps": "4350.vcc65d4958821", "git": "5.10.1"}
            )
        },
    },
    {
        # Test Case 3: Log analysis - Exact error matching
        "question": "What is the specific error message in the build logs?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 10, "status": "FAILURE"},
                    "build_logs": "ERROR: script returned exit code 127\nsh: 1: make: not found\nFinished: FAILURE",
                }
            )
        },
    },
    {
        # Test Case 4: Reading specific file contents
        "question": "What does the 'test' script do in my package.json?",
        "dummy_context": {
            "get_workspace_tree": "=== Workspace ID: 1 ===\n- package.json",
            "get_workspace_file": json.dumps(
                {"scripts": {"test": "jest --passWithNoTests"}}
            ),
        },
    },
    {
        # Test Case 5: Node resource extraction
        "question": "How much free memory is reported on the master node?",
        "dummy_context": {
            "get_general_jenkins_context": json.dumps(
                {"master_node": {"system_info": {"free_memory_mb": 420}}}
            )
        },
    },
    # ==========================================
    # HALLUCINATION TRAPS (The agent MUST NOT use pre-trained knowledge)
    # ==========================================
    {
        # Test Case 6: Missing Plugin Trap
        # The agent knows what Kubernetes is, but it's NOT in the context. It must say it's not installed.
        "question": "Is the kubernetes plugin installed and ready to use?",
        "dummy_context": {
            "get_installed_plugin_list": json.dumps(
                {
                    "git": "5.10.1",
                    "docker-workflow": "1.28",
                    # Kubernetes intentionally missing
                }
            )
        },
    },
    {
        # Test Case 7: Counter-intuitive Fact Trap
        # The user asks about the testing command. The agent's pre-trained knowledge
        # might expect 'npm test' or 'mvn test', but the actual Jenkinsfile contains
        # a completely unrelated or dummy command. The agent MUST faithfully report the dummy command.
        "question": "What command is being executed in the 'Test' stage of my Jenkinsfile?",
        "dummy_context": {
            "get_workspace_tree": "=== Workspace ID: default ===\n- Jenkinsfile",
            "get_workspace_file": "pipeline {\n  agent any\n  stages {\n    stage('Test') {\n      steps {\n        sh 'echo \"Skipping tests for now to save time\"'\n      }\n    }\n  }\n}",
        },
    },
    {
        # Test Case 8: Missing Detail Trap
        # The user asks a highly specific question ("Which user?"). The build was indeed
        # aborted, but the provided context does NOT contain the user's name.
        # The agent must state that the information is missing, rather than hallucinating a name like 'admin'.
        "question": "I see build #42 was aborted. Which user manually aborted it?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {
                        "number": 42,
                        "status": "ABORTED",
                        "causes": ["Started by upstream project 'Trigger-Job'"],
                        # No user is mentioned in the causes or logs
                    },
                    "build_logs": "Build was aborted\nFinished: ABORTED",
                }
            )
        },
    },
    {
        # Test Case 9: Missing File Trap
        # Agent must admit the file does not exist instead of guessing its contents.
        "question": "What dependencies are listed in my pom.xml?",
        "dummy_context": {
            "get_workspace_tree": "=== Workspace ID: 5 ===\n- src/\n- README.md",
            "get_workspace_file": "Error: File 'pom.xml' not found in workspace.",
        },
    },
    {
        # Test Case 10: Unrelated Log Trap
        # The user asks about a database error, but the logs only show a timeout.
        "question": "Did the build fail because of a database connection timeout?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 2, "status": "FAILURE"},
                    "build_logs": "npm ERR! code ELIFECYCLE\nFinished: FAILURE",
                }
            )
        },
    },
    # ==========================================
    # COMPLEX REASONING WITHOUT FABRICATION
    # ==========================================
    {
        # Test Case 11: Tree vs File mismatch
        "question": "Can you check the 'deploy.sh' file to see what server it deploys to?",
        "dummy_context": {
            "get_workspace_tree": "=== Workspace ID: 9 ===\n- deploy.sh",
            "get_workspace_file": "echo 'Deploying to staging server...'\nexit 0",
        },
    },
    {
        # Test Case 12: Ambiguous Build Status
        "question": "Did the build fail?",
        "dummy_context": {
            "get_build_details": json.dumps(
                {
                    "build_details": {"number": 100, "status": "UNSTABLE"},
                    "build_logs": "Tests passing: 99/100\nMarking build as UNSTABLE.",
                }
            )
        },
    },
    {
        # Test Case 13: Pipeline Configuration Inspection
        "question": "Does my pipeline use a global agent or none?",
        "dummy_context": {
            "get_job_details": json.dumps(
                {
                    "config_xml": "pipeline {\n  agent none\n  stages {\n    stage('Test') {\n      agent any\n    }\n  }\n}"
                }
            )
        },
    },
    {
        # Test Case 14: Job trigger inspection
        "question": "Is this job triggered by a GitHub webhook?",
        "dummy_context": {
            "get_job_details": json.dumps(
                {
                    "config_xml": "<flow-definition>\n  <triggers>\n    <hudson.triggers.TimerTrigger>\n      <spec>H/15 * * * *</spec>\n    </hudson.triggers.TimerTrigger>\n  </triggers>\n</flow-definition>"
                }
            )  # It's a cron job, not a webhook
        },
    },
    {
        # Test Case 15: Handling Empty Responses
        "question": "What is the system message on the master node?",
        "dummy_context": {
            "get_general_jenkins_context": json.dumps({"system_message": None})
        },
    },
]

CONTEXT_RECALL_TEST_CASES = [
    {
        "query": "declarative pipeline docker agent setup",
        "expected_output": "A Docker agent in a declarative pipeline is configured using the 'agent { docker { image ... } }' block.",
    },
    {
        "query": "scripted pipeline catch exception",
        "expected_output": "In a scripted pipeline, exceptions are handled using standard Groovy try-catch blocks.",
    },
    {
        "query": "parallel stages declarative pipeline",
        "expected_output": "Declarative pipelines support executing stages simultaneously by grouping them inside a 'parallel' block.",
    },
    {
        "query": "matrix build declarative pipeline variables",
        "expected_output": "A matrix directive allows running the same stages across multiple combinations of variables, axes, and tools.",
    },
    {
        "query": "environment variables declarative pipeline",
        "expected_output": "Environment variables are defined within the 'environment' block and accessed using the 'env.' prefix.",
    },
    {
        "query": "post build actions success failure always",
        "expected_output": "The 'post' directive allows executing steps conditionally based on the build status such as success, failure, or always.",
    },
    {
        "query": "parameters directive string boolean",
        "expected_output": "The 'parameters' directive defines user inputs like string, boolean, or choice values before a pipeline runs.",
    },
    {
        "query": "jenkinsfile stash unstash workspace",
        "expected_output": "The 'stash' and 'unstash' commands are used to securely pass files between different nodes or stages in a pipeline.",
    },
    # --- Category: Common Jenkins Plugins ---
    {
        "query": "kubernetes plugin pod template",
        "expected_output": "The Kubernetes plugin requires a Pod template defining the containers to be dynamically provisioned as Jenkins agents.",
    },
    {
        "query": "git plugin branch specifier wildcard",
        "expected_output": "The Git plugin allows specifying branches to build using the Branch Specifier field, which accepts exact names or wildcards.",
    },
    {
        "query": "credentials binding plugin secret text",
        "expected_output": "The Credentials Binding plugin allows injecting secret text or files into pipelines using the 'withCredentials' wrapper.",
    },
    {
        "query": "jenkins workspace cleanup plugin before after",
        "expected_output": "The Workspace Cleanup plugin can be configured to delete the workspace directory either before the build starts or after it finishes.",
    },
    {
        "query": "jenkins role based authorization strategy",
        "expected_output": "The Role-Based Authorization Strategy plugin allows defining access permissions based on global, project, or node roles.",
    },
    {
        "query": "script-security plugin manual approve",
        "expected_output": "The Script Security plugin requires administrators to manually approve unsandboxed Groovy methods before they can run in pipelines.",
    },
    {
        "query": "sonarqube scanner integration withSonarQubeEnv",
        "expected_output": "The SonarQube integration requires configuring the server in global settings and wrapping the analysis step inside 'withSonarQubeEnv'.",
    },
    {
        "query": "jenkins email extension plugin config",
        "expected_output": "The Email Extension plugin allows sending customized email notifications with build logs, dynamic triggers, and attachments.",
    },
    # --- Category: Error Handling & Troubleshooting ---
    {
        "query": "java.lang.OutOfMemoryError heap space maven",
        "expected_output": "A Java heap space OutOfMemoryError during a Maven build can usually be fixed by increasing the MAVEN_OPTS memory allocation.",
    },
    {
        "query": "npm ERR code ELIFECYCLE exit status 1",
        "expected_output": "An npm ELIFECYCLE exit status 1 indicates that a specific script defined in the package.json failed during execution.",
    },
    {
        "query": "jenkins master node offline executors",
        "expected_output": "When the Jenkins master node is offline, no builds can be scheduled unless distributed to available online agent nodes.",
    },
    {
        "query": "jenkins jnlp agent connection refused",
        "expected_output": "JNLP agents connect to the master via inbound TCP connections; connection refused usually implies the master's TCP port is blocked.",
    },
    {
        "query": "github webhook trigger jenkins 403 forbidden",
        "expected_output": "A 403 Forbidden error on a GitHub webhook trigger often means Jenkins lacks anonymous read access or a valid webhook secret.",
    },
    {
        "query": "pipeline timeout directive abort",
        "expected_output": "The timeout directive sets a maximum execution time for a stage or the entire pipeline, after which the process is forcefully aborted.",
    },
    # --- Category: Global Configuration & Architecture ---
    {
        "query": "cron syntax trigger pipeline schedule",
        "expected_output": "Pipeline triggers can be scheduled periodically using standard cron syntax in the 'triggers { cron() }' directive.",
    },
    {
        "query": "jenkins shared libraries global reuse",
        "expected_output": "Global Shared Libraries in Jenkins allow sharing reusable Groovy code, functions, and pipeline wrappers across multiple jobs.",
    },
    {
        "query": "archiveArtifacts declarative pipeline syntax",
        "expected_output": "The 'archiveArtifacts' step saves specific files generated by the build on the master node for later user access.",
    },
    {
        "query": "jenkins API token creation user config",
        "expected_output": "API tokens can be created in the Jenkins user configuration page to securely authenticate external REST API calls.",
    },
    {
        "query": "webhook github trigger GITScm polling",
        "expected_output": "To trigger a Jenkins job automatically via GitHub webhook, the 'GitHub hook trigger for GITScm polling' option must be checked.",
    },
    {
        "query": "dockerfile agent additionalBuildArgs",
        "expected_output": "When using a Dockerfile as an agent, custom build arguments can be passed using the 'additionalBuildArgs' parameter.",
    },
    {
        "query": "jenkins backup thinbackup plugin schedule",
        "expected_output": "The ThinBackup plugin provides lightweight, scheduled backups of the Jenkins global configurations and job specific XMLs.",
    },
    {
        "query": "replay pipeline jenkins UI modify",
        "expected_output": "The Replay feature in the Jenkins UI allows modifying a pipeline script of a past build and re-executing it immediately without committing.",
    },
]

PERFORMANCE_TEST_CASES = [
    {
        # Scenario 1: Basic System Information
        # Very lightweight query accessing only top-level context fields.
        "query": "What is the current Jenkins version and is there any active system message?",
        "max_latency": 10.0,
        "max_cost": 0.005,
    },
    {
        # Scenario 2: Agent and Hardware Statistics
        # Requires the agent to parse the nested 'agent_stats' and 'master_node' dictionaries.
        "query": "How many agents are currently online, and how much free memory does the Linux master node have?",
        "max_latency": 12.0,
        "max_cost": 0.006,
    },
    {
        # Scenario 3: Plugin Verification
        # Requires the agent to scan the 'active_plugins' dictionary for a specific key.
        "query": "Can you check my active plugins and tell me if the Kubernetes plugin is installed? If so, what version?",
        "max_latency": 12.0,
        "max_cost": 0.008,
    },
    {
        # Scenario 4: Build Metadata Extraction
        # Parses the 'build_details' object to extract specific metadata without touching the heavy logs.
        "query": "Did build number 104 succeed? Also, how long did it take and who originally triggered it?",
        "max_latency": 12.0,
        "max_cost": 0.008,
    },
    {
        # Scenario 5: Job Configuration Details
        # Slightly heavier as it requires inspecting the 'job_details' object which typically contains the config_xml.
        "query": "I am looking at the 'backend-api-pipeline' job. Is this a Pipeline job and is it currently buildable?",
        "max_latency": 15.0,
        "max_cost": 0.010,
    },
]
