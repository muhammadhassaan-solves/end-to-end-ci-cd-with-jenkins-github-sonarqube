pipeline {
    agent {
        // Use Docker-in-Docker image
        docker {
            image 'docker:20.10.16-dind'
            // Privileged mode + mount Docker socket
            args '--privileged -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    stages {
        stage('Install Tools') {
            steps {
                // The docker:dind image is Alpine-based and doesn't include Java/Maven.
                // So we install them here.
                sh '''
                  apk update
                  apk add openjdk11 maven
                '''
            }
        }

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
                // Now we can run Docker commands inside the container
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
            // Clean up container
            sh 'docker stop java_app || true'
            sh 'docker rm java_app || true'
        }
    }
}
