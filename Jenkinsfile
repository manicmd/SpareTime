/**
 * JenkinsFile for the CI and CD pipeline.
 * ~~ MANAGED BY DEVOPS ~~
 */

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
                script { echo 'running sample script '
                }
            }
        }
        stage('Initialise') {
        }
        stage('Prepare') {
            agent {
                label 'windows'
            }
            when {
                expression {1==1}
            }
            steps {
                script {
                     echo "RUNNING... PREPARING STAGE .....  ${env.BUILD_NUMBER}"
                }
            }
        }
        stage('Production') {
        }
    }
}