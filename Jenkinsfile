pipeline {
    options {
        skipDefaultCheckout(true)  // Avoid automatic SCM checkout
    }
    agent none  // We'll specify agents per stage

    stages {
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
                sh '''
                    echo "Starting Build & Test..."
                    start_time=$(date +%s)

                    mvn clean compile
                    mvn test
                    mvn package

                    end_time=$(date +%s)
                    build_time=$((end_time - start_time))
                    echo "Build time (seconds): $build_time"

                    # Write the build time to a file
                    echo $build_time > build_time.txt

                    # Log to MLflow, passing build_time as an argument
                    python3 log_build_time.py $(cat build_time.txt)
                '''
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

                        # Optionally run the JAR in the background on EC2
                        ssh -i $SSH_KEY ubuntu@44.202.146.87 "nohup java -jar cicd-jenkins-mlflow-1.0-SNAPSHOT.jar > output.log 2>&1 &"

                        end_time=$(date +%s)
                        deploy_time=$((end_time - start_time))
                        echo "Deploy time (seconds): $deploy_time"

                        # Write the deploy time to a file
                        echo $deploy_time > deploy_time.txt

                        # Log to MLflow, passing deploy_time as an argument
                        python3 log_deploy_time.py $(cat deploy_time.txt)
                    '''
                }
            }
        }
    }
}
