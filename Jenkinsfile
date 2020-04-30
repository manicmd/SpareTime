pipeline {

    agent none

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