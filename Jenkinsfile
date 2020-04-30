/**
 * JenkinsFile for the CI and CD pipeline of Test.io.
 * ~~ MANAGED BY DEVOPS ~~
 */

/**
 * By default the master branch of the library is loaded
 * Use the include directive below ONLY if you need to load a branch of the library
 * @Library('intellifloworkflow@IP-22228')
 */
import org.intelliflo.*

def changesetJson = new String()
def changeset = new Changeset()

def globals = env
def nodeTags = 'uitest'
def sonarServer = 'https://sonar.intelliflo.io/'
def sonarLogin = '34ea144c75c5489c4f6083f6cf94f7bc7ae217d2'
def gitCredentialsId = '1327a29c-d426-4f3d-b54a-339b5629c041'
def jiraCredentialsId = '32546070-393c-4c45-afcd-8e8f1de1757b'
def semanticVersion
def packageVersion
def verboseLogging = false
def stageName

pipeline {

    agent none

    environment {
        githubRepoName = "${env.JOB_NAME.split('/')[1]}"
    }

    options {
        timestamps()
        skipDefaultCheckout()
    }

    stages {
        stage('Master') {
            when {
                branch 'master'
            }
            steps {
                script {
                    triggerRepoScan {
                        credentialsId = gitCredentialsId
                    }
                }
            }
        }

        stage('Initialise') {
            agent none
            when {
                expression { env.BRANCH_NAME ==~ /^(IP-|PR-).*/ }
            }
            steps {
                script {
                    stashResourceFiles {
                        targetPath = 'org/intelliflo'
                        masterNode = 'master'
                        stashName = 'ResourceFiles'
                        resourcePath = "@libs/intellifloworkflow/resources"
                    }

                    abortOlderBuilds {
                        logVerbose = verboseLogging
                    }
                }
            }
        }

        stage('Prepare') {
            agent {
                label 'windows'
            }
            when {
                expression { env.BRANCH_NAME ==~ /^(IP-|PR-).*/ }
            }
            steps {
                script {
                    stageName = 'Prepare'
                    validateChangeset {
                        repoName = globals.githubRepoName
                        prNumber = globals.CHANGE_ID
                        baseBranch = globals.CHANGE_TARGET
                        branchName = globals.BRANCH_NAME
                        buildNumber = globals.BUILD_NUMBER
                        logVerbose = verboseLogging
                        delegate.stageName = stageName
                        abortOnFailure = true
                    }
                    changesetJson = (String)Consul.getStoreValue(ConsulKey.get(globals.githubRepoName, globals.BRANCH_NAME, globals.CHANGE_ID, 'changeset'))
                    changeset = changeset.fromJson(changesetJson)

                    // Scripts required by the pipeline
                    unstashResourceFiles {
                        folder = 'pipeline'
                        stashName = 'ResourceFiles'
                    }

                    // Versioning
                    calculateVersion {
                        buildNumber = globals.BUILD_NUMBER
                        delegate.changeset = changeset
                        delegate.stageName = stageName
                        abortOnFailure = true
                    }

                    semanticVersion = Consul.getStoreValue(ConsulKey.get(globals.githubRepoName, globals.BRANCH_NAME, globals.CHANGE_ID, 'existing.version'))
                    packageVersion = "${semanticVersion}.${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Python-Lint') {
            agent  none
            when {
                expression { env.BRANCH_NAME ==~ /^(IP-|PR-).*/ }
            }
            steps {
                script {
                    node(nodeTags) {
                        stageName = 'Python-Lint'
                        checkoutCode {
                            delegate.stageName = stageName
                        }

                        if (changeset.pullRequest != null) {
                            currentBuild.displayName = "${githubRepoName}.Pr${changeset.prNumber}(${packageVersion})"
                        } else {
                            currentBuild.displayName = "${githubRepoName}(${packageVersion})"
                        }

                        sh "mkdir dist"

                        try {
                            sh """
                                pylint ./userjourneys -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > dist/pylint-report.txt
                            """
                        }
                        catch (Exception ex) {
                            echo ex.getMessage()
                            echo "[ERROR] Pylint failed. Look at pylint-report.txt in artifacts for more details"
                        }

                        Boolean runSonarQube = false
                        def runSonarQubeOverride = Boolean.valueOf(Consul.getStoreValue("pipelineconfig/run.sonarqube"))

                        if (runSonarQubeOverride == true) {
                            def sonarScannerHome = tool 'SonarScanner'
                            def sonarScanner = "${sonarScannerHome}/bin/sonar-scanner"
                            echo "[INFO] Initialising SonarQube Analysis sonarScanner=${sonarScanner}"
                            sh """
                                ${sonarScanner} \
                                -Dsonar.projectKey=${globals.githubRepoName} \
                                -Dsonar.projectName=${globals.githubRepoName} \
                                -Dsonar.projectVersion=${semanticVersion} \
                                -Dsonar.sources=${pwd()} \
                                -Dsonar.host.url=${sonarServer} \
                                -Dsonar.projectKey=${globals.githubRepoName} \
                                -Dsonar.python.pylint.reportPath=/bin/pylint \
                                -Dsonar.login=${sonarLogin} \
                            """
                        }

                        archive includes: 'dist/*.*'
                        deleteDir()
                    }
                }
            }
        }

        stage('Production') {
            agent  none
            when {
                expression { env.BRANCH_NAME ==~ /^PR-.*/ }
            }
            steps {
                script {
                    validateCodeReviews {
                        repoName = globals.githubRepoName
                        prNumber = globals.CHANGE_ID
                        author = changeset.author
                        failBuild = false
                        codeReviewApprovalTeam = 'ui-test-automation'
                        logVerbose = verboseLogging
                        delegate.stageName = stageName
                    }

                    validateJiraTicket {
                        delegate.changeset = changeset
                        failBuild = false
                        delegate.stageName = stageName
                        logVerbose = verboseLogging
                    }

                    validateMasterSha {
                        repoName = changeset.repoName
                        packageMasterSha = changeset.masterSha
                        logVerbose = verboseLogging
                        delegate.stageName = stageName
                    }

                    mergePullRequest {
                        repoName = changeset.repoName
                        prNumber = changeset.prNumber
                        masterSha = changeset.masterSha
                        sha = changeset.commitSha
                        consulKey = changeset.consulBaseKey
                        credentialsId = gitCredentialsId
                        logVerbose = true
                        delegate.stageName = stageName
                    }

                    updateMasterVersion {
                        repoName = changeset.repoName
                        version = semanticVersion
                        logVerbose = verboseLogging
                        delegate.stageName = stageName
                    }

                    tagCommit {
                        repoName = changeset.repoName
                        version = semanticVersion
                        author = changeset.author
                        email = changeset.commitInfo.author.email
                        logVerbose = verboseLogging
                        delegate.stageName = stageName
                    }

                    updateJiraOnMerge {
                        issueKey = changeset.jiraTicket
                        packageName = changeset.repoName
                        version = packageVersion
                        credentialsId = jiraCredentialsId
                        logVerbose = verboseLogging
                        delegate.stageName = stageName
                    }

                    cleanupConsul {
                        repoName = changeset.repoName
                        prNumber = changeset.prNumber
                        consulBuildKey = changeset.consulBuildKey
                        logVerbose = verboseLogging
                        delegate.stageName = stageName
                    }

                    deleteGithubBranch {
                        repoName = changeset.repoName
                        branchName = changeset.originatingBranch
                        logVerbose = verboseLogging
                    }
                }
            }
        }
    }
}