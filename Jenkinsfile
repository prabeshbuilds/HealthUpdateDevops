pipeline {
    agent any

    environment {
        IMAGE_NAME = "health-update-project-web"
        DOCKERHUB_USER = "your_dockerhub_username"   // 🔁 Replace this
    }

    stages {

        stage('Checkout Code') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    rm -rf venv
                    python3 -m venv venv
                    chmod -R 755 venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Lint') {
            steps {
                sh '''
                    venv/bin/pip install flake8
                    venv/bin/flake8 . || true
                '''
            }
        }

        stage('Run Django Tests') {
            steps {
                sh '''
                    venv/bin/python manage.py test
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $IMAGE_NAME:latest .
                '''
            }
        }

    }

    post {
        success {
            echo '✅ CI Pipeline Succeeded'
        }
        failure {
            echo '❌ CI Pipeline Failed'
        }
        always {
            sh 'docker logout || true'
            cleanWs()
        }
    }
}