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

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-java-app .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 8080:8080 --name java_app my-java-app'
            }
        }

        stage('Deploy') {
            steps {
                echo "Application is running at http://localhost:8080/HelloWorld"
            }
        }
    }

    post {
        always {
            sh 'docker stop java_app || true'
            sh 'docker rm java_app || true'
        }
    }
}
