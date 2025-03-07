pipeline {
    agent none

    stages {
        stage('Build & Test in Docker') {
            agent {
                docker {
                    // Use Maven + OpenJDK 11 image
                    image 'maven:3.8.6-openjdk-11'
                    // Run as root to avoid file permission issues when cleaning target/
                    args '-u root'
                }
            }
            steps {
                // Jenkins automatically checks out your code on the host
                // Then bind-mounts the workspace into the container
                // Now run maven commands as root user in the container
                sh 'mvn clean compile'
                sh 'mvn test'
                sh 'mvn package'
            }
        }

        stage('Run in Docker') {
            agent {
                docker {
                    image 'maven:3.8.6-openjdk-11'
                    args '-u root'
                }
            }
            steps {
                // Run the newly built JAR in the container
                // The ampersand (&) runs it in the background
                sh 'java -jar target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar &'
            }
        }

        stage('Deploy from Jenkins Host') {
            // Use the Jenkins host, which has the SSH key (new.pem)
            agent any
            steps {
                echo 'Deploying to EC2 from Jenkins host...'
                sh '''
                    # Make sure your key is in the workspace, or in a known path on Jenkins
                    chmod 400 new.pem

                    # Copy the JAR file to EC2
                    scp -i new.pem target/cicd-jenkins-mlflow-1.0-SNAPSHOT.jar ubuntu@44.202.146.87:~

                    # Run the JAR in the background on EC2
                    ssh -i new.pem ubuntu@44.202.146.87 "nohup java -jar cicd-jenkins-mlflow-1.0-SNAPSHOT.jar > output.log 2>&1 &"
                '''
            }
        }
    }
}
