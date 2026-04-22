pipeline {
    agent any

    environment {
        IMAGE_NAME = "health_update_project-web:latest"
        VENV = "venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('Create Clean Virtual Environment') {
            steps {
                sh '''
                    rm -rf venv
                    python3 -m venv venv
                    chmod -R 755 venv
                    venv/bin/python -m pip install --upgrade pip
                    venv/bin/pip install -r requirements.txt
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
            cleanWs()
        }
    }
}