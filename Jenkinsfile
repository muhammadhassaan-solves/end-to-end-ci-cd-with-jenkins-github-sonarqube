pipeline {
    agent none

    stages {
        stage('Build & Test in Docker') {
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                }
            }
            steps {
                sh 'mvn clean compile'
                sh 'mvn test'
                sh 'mvn package'
            }
        }

        stage('Run in Docker') {
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                }
            }
            steps {
                sh 'java -jar target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar &'
            }
        }

        stage('Deploy from Jenkins Host') {
            agent any
            steps {
                sh '''
                    chmod 400 new.pem
                    scp -i new.pem target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar ubuntu@44.202.146.87:~
                    ssh -i new.pem ubuntu@44.202.146.87 "nohup java -jar cicd-jenkins-mlflow-1.0-SNAPSHOT.jar > output.log 2>&1 &"
                '''
            }
        }
    }
}
