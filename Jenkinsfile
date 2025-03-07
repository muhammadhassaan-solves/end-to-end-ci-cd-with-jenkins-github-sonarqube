pipeline {
    agent {
        docker {
            image 'maven:3.8.6-openjdk-11'
        }
    }

    stages {  
        stage('Build') {
            steps {
                sh 'mvn clean compile'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }

        stage('Package') {
            steps {
                sh 'mvn package'
            }
        }

        stage('Run') {
            steps {
                sh 'java -jar target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar &'
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying application..."
                // Add your deployment script/command here
            }
        }
    }
}
