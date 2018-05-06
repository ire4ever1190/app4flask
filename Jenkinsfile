    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                tox
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                tox
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                tox
            }
        }
    }
