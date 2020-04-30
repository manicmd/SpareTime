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
    }
}