pipeline {

    agent none

    stages {
        stage('Master') {
        echo "running master stage .... "
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