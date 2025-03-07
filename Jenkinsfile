pipeline {
    // Prevent Jenkins from automatically checking out code on the host
    options {
        skipDefaultCheckout(true)
    }
    agent none  // We'll define the agent in each stage

    stages {
        stage('Checkout Code in Docker') {
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    // Run as root to avoid file permission issues
                    args '-u root'
                }
            }
            steps {
                // Clone your repo INSIDE the container
                sh 'git clone -b main https://github.com/muhammadhassaan-solves/CI-CD-Pipeline-Optimization-using-Jenkins-and-MLflow.git .'
            }
        }

        stage('Build & Test in Docker') {
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    args '-u root'
                }
            }
            steps {
                sh 'mvn clean compile'
                sh 'mvn test'
                sh 'mvn package'
            }
        }

        stage('Deploy from Jenkins Host') {
            // We'll deploy on the host to access the SSH key via Jenkins Credentials
            agent any
            steps {
                withCredentials([file(credentialsId: 'EC2_SSH_KEY', variable: 'SSH_KEY')]) {
                    sh '''
                        echo "Deploying to EC2..."
                        chmod 400 $SSH_KEY
                        scp -i $SSH_KEY target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar ubuntu@44.202.146.87:~
                        ssh -i $SSH_KEY ubuntu@44.202.146.87 "nohup java -jar cicd-jenkins-mlflow-1.0-SNAPSHOT.jar > output.log 2>&1 &"
                    '''
                }
            }
        }
    }
}
