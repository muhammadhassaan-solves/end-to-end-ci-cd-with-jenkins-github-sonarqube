pipeline {
    options {
        skipDefaultCheckout(true)
    }
    agent none

    stages {
        stage('Checkout Code') {
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    args '-u root -v $HOME/.m2:/root/.m2'  // Cache Maven deps
                }
            }
            steps {
                cleanWs()
                git(
                    url: 'https://github.com/muhammadhassaan-solves/CI-CD-Pipeline-Optimization-using-Jenkins-and-Mlflow.git',
                    branch: 'main'
                )
            }
        }

        stage('Build & Test') {
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    args '-u root -v $HOME/.m2:/root/.m2'
                }
            }
            steps {
                script {
                    def startBuild = System.currentTimeMillis()
                    sh 'mvn clean compile test package'
                    def buildDuration = (System.currentTimeMillis() - startBuild)/1000
                    env.BUILD_TIME = buildDuration
                }
            }
        }

        stage('MLflow Tracking') {
            agent {
                docker {
                    image 'python:3.9-slim'
                    args '-u root'
                }
            }
            steps {
                script {
                    sh """
                    pip install mlflow scikit-learn
                    python -c \"import mlflow; 
                        mlflow.set_tracking_uri('http://your-mlflow-server:5000');
                        mlflow.start_run();
                        mlflow.log_metric('build_time', ${env.BUILD_TIME});
                        mlflow.log_param('commit_id', '${GIT_COMMIT}');
                        mlflow.end_run()\"
                    """
                }
            }
        }

        stage('Deploy') {
            agent any
            steps {
                script {
                    def startDeploy = System.currentTimeMillis()
                    withCredentials([file(credentialsId: '4c7e72da-f3f3-40a6-ab52-8650693969fa', variable: 'SSH_KEY')]) {
                        sh """
                        scp -i $SSH_KEY -o StrictHostKeyChecking=no target/*.jar ubuntu@44.202.146.87:~/app.jar
                        ssh -i $SSH_KEY ubuntu@44.202.146.87 'nohup java -jar app.jar > log.txt 2>&1 &'
                        """
                    }
                    def deployDuration = (System.currentTimeMillis() - startDeploy)/1000
                    // Log deploy time to MLflow similarly
                }
            }
        }
    }
}
