pipeline {
    // We do NOT want Jenkins automatically checking out code
    agent none
    options {
        skipDefaultCheckout(true)  // Disable default SCM checkout
    }

    stages {
        // (Optional) Clean workspace permissions to avoid AccessDenied
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
                    // Measure build time in seconds
                    def startTime = System.currentTimeMillis()
                    
                    sh 'mvn clean compile'
                    sh 'mvn test'
                    sh 'mvn package'
                    
                    def endTime = System.currentTimeMillis()
                    def buildTime = (endTime - startTime) / 1000

                    // Save build time to a file
                    sh "echo ${buildTime} > build_time.txt"

                    // Log build time to MLflow (runs on Jenkins host)
                    sh "/var/lib/jenkins/mlflow_venv/bin/python3 /var/lib/jenkins/log_build_time.py $(cat build_time.txt)"
                }
            }
        }

        stage('Deploy from Jenkins Host') {
            agent any
            steps {
                script {
                    // Measure deploy time in seconds
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

                    // Save deploy time to a file
                    sh "echo ${deployTime} > deploy_time.txt"

                    // Log deploy time to MLflow (runs on Jenkins host)
                    sh "/var/lib/jenkins/mlflow_venv/bin/python3 /var/lib/jenkins/log_deploy_time.py $(cat deploy_time.txt)"
                }
            }
        }
    }
}
