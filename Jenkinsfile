pipeline {
    options {
        skipDefaultCheckout(true)
    }
    agent none

    stages {
        stage('Checkout Code in Docker') {
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    args '-u root'
                }
            }
            steps {
                sh 'rm -rf ./* .git*'
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
                sh 'echo "Starting Build & Test..."'
                sh 'start_time=$(date +%s)'
                sh 'mvn clean compile'
                sh 'mvn test'
                sh 'mvn package'
                sh 'end_time=$(date +%s)'
                sh 'echo $(($end_time - $start_time)) > build_time.txt'
                sh 'python3 log_build_time.py'
            }
        }

        stage('Deploy from Jenkins Host') {
            agent any
            steps {
                withCredentials([file(credentialsId: '4c7e72da-f3f3-40a6-ab52-8650693969fa', variable: 'SSH_KEY')]) {
                    sh '''
                        echo "Deploying to EC2..."
                        start_time=$(date +%s)
                        chmod 400 $SSH_KEY
                        scp -i $SSH_KEY target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar ubuntu@44.202.146.87:~
                        ssh -i $SSH_KEY ubuntu@44.202.146.87 "nohup java -jar cicd-jenkins-mlflow-1.0-SNAPSHOT.jar > output.log 2>&1 &"
                        end_time=$(date +%s)
                        echo $(($end_time - $start_time)) > deploy_time.txt
                        python3 log_deploy_time.py
                    '''
                }
            }
        }
    }
}
