pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/muhammadhassaan-solves/CI-CD-Pipeline-Optimization-using-Jenkins-and-MLflow'
        BRANCH = 'main'
        IMAGE_NAME = 'maven:3.8.6-openjdk-11'
        DEPLOY_USER = 'ubuntu'
        DEPLOY_HOST = '44.202.146.87'
        JAR_FILE = 'cicd-jenkins-mlflow-1.0-SNAPSHOT.jar'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${BRANCH}", url: "${REPO_URL}"
            }
        }

        stage('Build & Test in Docker') {
            steps {
                script {
                    docker.image("${IMAGE_NAME}").inside {
                        sh 'mvn clean compile'
                    }
                }
            }
        }

        stage('Package Artifact') {
            steps {
                script {
                    docker.image("${IMAGE_NAME}").inside {
                        sh 'mvn package'
                    }
                }
            }
        }

        stage('Deploy from Jenkins Host') {
            steps {
                withCredentials([file(credentialsId: 'EC2_SSH_KEY', variable: 'SSH_KEY')]) {
                    sh '''
                        chmod 400 $SSH_KEY
                        scp -i $SSH_KEY target/$JAR_FILE $DEPLOY_USER@$DEPLOY_HOST:~
                        ssh -i $SSH_KEY $DEPLOY_USER@$DEPLOY_HOST "nohup java -jar $JAR_FILE > output.log 2>&1 &"
                    '''
                }
            }
        }
    }
}
