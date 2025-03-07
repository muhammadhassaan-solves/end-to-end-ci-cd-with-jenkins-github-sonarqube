pipeline {
    agent none
    options {
        skipDefaultCheckout(true)  // No default SCM checkout
    }

    stages {
        stage('Fix Permissions') {
            agent any
            steps {
                sh '''
                    echo "Fixing workspace permissions..."
                    sudo chown -R jenkins:jenkins /var/lib/jenkins/workspace/javaapp || true
                    sudo chmod -R 775 /var/lib/jenkins/workspace/javaapp || true
                    sudo rm -f /var/lib/jenkins/workspace/javaapp/.git/config.lock || true
                '''
            }
        }

        stage('Checkout Code in Docker') {
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    args '-u root'
                }
            }
            steps {
                sh '''
                    echo "Cleaning workspace..."
                    rm -rf ./* .git*

                    echo "Cloning repository..."
                    git clone -b main https://github.com/muhammadhassaan-solves/CI-CD-Pipeline-Optimization-using-Jenkins-and-MLflow.git .
                '''
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
                script {
                    // Measure build time
                    def startTime = System.currentTimeMillis()
                    sh 'mvn clean compile'
                    sh 'mvn test'
                    sh 'mvn package'
                    def endTime = System.currentTimeMillis()
                    def buildTime = (endTime - startTime) / 1000

                    // Write build time to a file
                    sh "echo ${buildTime} > build_time.txt"

                    // Read from file into a variable
                    def buildTimeVal = sh(script: 'cat build_time.txt', returnStdout: true).trim()

                    // Log build time to MLflow
                    sh "/var/lib/jenkins/mlflow_venv/bin/python3.12 /var/lib/jenkins/log_build_time.py"
                }
            }
        }

        stage('Deploy from Jenkins Host') {
            agent any
            steps {
                script {
                    def deployStart = System.currentTimeMillis()

                    withCredentials([file(credentialsId: '4c7e72da-f3f3-40a6-ab52-8650693969fa', variable: 'SSH_KEY')]) {
                        sh '''
                            echo "Deploying to EC2..."
                            chmod 400 $SSH_KEY
                            scp -i $SSH_KEY target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar ubuntu@44.202.146.87:~
                            ssh -i $SSH_KEY ubuntu@44.202.146.87 "nohup java -jar cicd-jenkins-mlflow-1.0-SNAPSHOT.jar > output.log 2>&1 &"
                        '''
                    }

                    def deployEnd = System.currentTimeMillis()
                    def deployTime = (deployEnd - deployStart) / 1000

                    // Write deploy time to a file
                    sh "echo ${deployTime} > deploy_time.txt"

                    // Read from file into a variable
                    def deployTimeVal = sh(script: 'cat deploy_time.txt', returnStdout: true).trim()

                    // Log deploy time to MLflow
                    sh "/var/lib/jenkins/mlflow_venv/bin/python3.12 /var/lib/jenkins/log_deploy_time.py"
                }
            }
        }
    }
}
