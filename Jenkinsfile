pipeline {
    agent any
    environment {
        // Set the correct virtual environment path
        VIRTUAL_ENV = '/var/lib/jenkins/mlflow_venv'
        // Set your EC2 deployment details
        DEPLOY_HOST = '44.202.146.87'
        DEPLOY_USER = 'ubuntu'
        ARTIFACT_NAME = 'cicd-jenkins-mlflow-1.0-SNAPSHOT.jar'
    }
    stages {
        stage('Checkout Code') {
            steps {
                // Checkout your code from source control
                checkout scm
            }
        }
        stage('Build') {
            steps {
                // For example, using Maven to build your project
                sh 'mvn clean package'
            }
        }
        stage('Log Build Time') {
            steps {
                // Run your Python script using the correct virtual environment path
                sh '$VIRTUAL_ENV/bin/python3 log_build_time.py 50.972'
            }
        }
        stage('Deploy to EC2') {
            agent any
            steps {
                // Use SSH key credentials to deploy the artifact to your EC2 instance
                withCredentials([file(credentialsId: '4c7e72da-f3f3-40a6-ab52-8650693969fa', variable: 'SSH_KEY')]) {
                    sh '''
                        echo "Deploying to EC2..."
                        chmod 400 $SSH_KEY
                        # Transfer the artifact to EC2
                        scp -o StrictHostKeyChecking=no -i $SSH_KEY target/${ARTIFACT_NAME} ${DEPLOY_USER}@${DEPLOY_HOST}:~
                        # Start the artifact (adjust the command as needed)
                        ssh -o StrictHostKeyChecking=no -i $SSH_KEY ${DEPLOY_USER}@${DEPLOY_HOST} "nohup java -jar ${ARTIFACT_NAME} > output.log 2>&1 &"
                    '''
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline completed."
        }
        failure {
            echo "Pipeline failed. Please review the logs."
        }
    }
}
