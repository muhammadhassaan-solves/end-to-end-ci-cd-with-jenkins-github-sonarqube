pipeline {
    agent none
    options {
        // Avoid Jenkins automatically checking out the repo
        skipDefaultCheckout(true)
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
            // We do the manual git clone inside Docker
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    // Run as root user to avoid permission issues
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

        stage('Show Git Commit (Optional)') {
            // Just to confirm the current commit
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    args '-u root'
                }
            }
            steps {
                script {
                    // This runs in the same Docker container with the .git folder
                    def commitId = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    echo "Current Git Commit: ${commitId}"
                }
            }
        }

        stage('Build & Test in Docker') {
            // Still inside Docker for building/testing
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    args '-u root'
                }
            }
            steps {
                script {
                    // Measure time in Bash
                    sh '''
                        echo "Starting Build & Test..."
                        start_time=$(date +%s)

                        mvn clean compile
                        mvn test
                        mvn package

                        end_time=$(date +%s)
                        build_time=$((end_time - start_time))
                        echo $build_time > build_time.txt
                    '''
                }
            }
        }

        stage('Log Build Time') {
            // Log to MLflow on the Jenkins host (NOT in Docker)
            agent any
            steps {
                script {
                    // Read build_time.txt from the workspace
                    def buildTimeVal = sh(script: 'cat build_time.txt', returnStdout: true).trim()

                    // Call Python in the venv to log build time
                    sh "/var/lib/jenkins/mlflow_venv/bin/python3 /var/lib/jenkins/log_build_time.py ${buildTimeVal}"
                }
            }
        }

        stage('Deploy from Jenkins Host') {
            // We deploy from the host to an EC2 instance
            agent any
            steps {
                script {
                    // Start measuring time
                    sh '''
                        deploy_start=$(date +%s)
                    '''

                    withCredentials([file(credentialsId: '4c7e72da-f3f3-40a6-ab52-8650693969fa', variable: 'SSH_KEY')]) {
                        sh '''
                            echo "Deploying to EC2..."
                            chmod 400 $SSH_KEY
                            scp -i $SSH_KEY target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar ubuntu@44.202.146.87:~
                            ssh -i $SSH_KEY ubuntu@44.202.146.87 "nohup java -jar cicd-jenkins-mlflow-1.0-SNAPSHOT.jar > output.log 2>&1 &"
                        '''
                    }

                    // End measuring time
                    sh '''
                        deploy_end=$(date +%s)
                        deploy_time=$((deploy_end - deploy_start))
                        echo $deploy_time > deploy_time.txt
                    '''
                }
            }
        }

        stage('Log Deploy Time') {
            // Again, log to MLflow on the Jenkins host
            agent any
            steps {
                script {
                    def deployTimeVal = sh(script: 'cat deploy_time.txt', returnStdout: true).trim()

                    // Use the Python binary in the venv
                    sh "/var/lib/jenkins/mlflow_venv/bin/python3 /var/lib/jenkins/log_deploy_time.py ${deployTimeVal}"
                }
            }
        }
    }
}
