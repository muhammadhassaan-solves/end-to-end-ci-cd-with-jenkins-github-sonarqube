pipeline {
    agent {
        docker {
            image 'maven:3.8.6-openjdk-11'
            // run as root so we can install packages
            args '-u root'
        }
    }

    stages {
        stage('Install SSH Client') {
            steps {
                sh 'apt-get update && apt-get install -y openssh-client'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean compile'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }

        stage('Package') {
            steps {
                sh 'mvn package'
            }
        }

        stage('Run') {
            steps {
                sh 'java -jar target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar &'
            }
        }

        stage('Deploy') {
            steps {
                // Make sure new.pem is in the workspace or mounted
                sh '''
                    chmod 400 new.pem
                    scp -i new.pem target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar ubuntu@44.202.146.87:~
                    ssh -i new.pem ubuntu@44.202.146.87 "nohup java -jar cicd-jenkins-mlflow-1.0-SNAPSHOT.jar > output.log 2>&1 &"
                '''
            }
        }
    }
}
