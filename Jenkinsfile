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
                    sh '''
                        echo "Starting build process..."
                        start_time=$(date +%s)

                        mvn clean compile
                        mvn test
                        mvn package

                        end_time=$(date +%s)
                        build_time=$((end_time - start_time))
                        echo $build_time > build_time.txt
                    '''

                    def buildTimeVal = sh(script: 'cat build_time.txt', returnStdout: true).trim()

                    // ✅ Use "." instead of "source"
                    sh '''
                        . /var/lib/jenkins/mlflow_venv/bin/activate
                        python /var/lib/jenkins/log_build_time.py ''' + buildTimeVal
                }
            }
        }

        stage('Deploy from Jenkins Host') {
            agent any
            steps {
                script {
                    sh '''
                        echo "Starting deployment..."
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

                    sh '''
                        deploy_end=$(date +%s)
                        deploy_time=$((deploy_end - deploy_start))
                        echo $deploy_time > deploy_time.txt
                    '''

                    def deployTimeVal = sh(script: 'cat deploy_time.txt', returnStdout: true).trim()

                    // ✅ Use "." instead of "source"
                    sh '''
                        . /var/lib/jenkins/mlflow_venv/bin/activate
                        python /var/lib/jenkins/log_deploy_time.py ''' + deployTimeVal
                }
            }
        }
    }
}
