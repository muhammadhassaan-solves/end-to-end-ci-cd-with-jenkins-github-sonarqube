stage('Build & Test in Docker') {
    agent {
        docker {
            image 'maven:3.8.6-openjdk-11'
            args '-u root'
        }
    }
    steps {
        script {
            def startTime = System.currentTimeMillis()
            sh 'mvn clean compile'
            sh 'mvn test'
            sh 'mvn package'
            def endTime = System.currentTimeMillis()
            def buildTime = (endTime - startTime) / 1000

            sh "echo ${buildTime} > build_time.txt"
            def buildTimeVal = sh(script: 'cat build_time.txt', returnStdout: true).trim()

            // Just call python3 in the venv directly
            sh "/var/lib/jenkins/mlflow_venv/bin/python3 /var/lib/jenkins/log_build_time.py ${buildTimeVal}"
        }
    }
}

stage('Deploy from Jenkins Host') {
    agent any
    steps {
        script {
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

            sh "echo ${deployTime} > deploy_time.txt"
            def deployTimeVal = sh(script: 'cat deploy_time.txt', returnStdout: true).trim()

            // Again, call python in the venv directly
            sh "/var/lib/jenkins/mlflow_venv/bin/python3 /var/lib/jenkins/log_deploy_time.py ${deployTimeVal}"
        }
    }
}
