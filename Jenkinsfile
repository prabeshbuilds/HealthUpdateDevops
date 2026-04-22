pipeline {
    agent any

    environment {
        IMAGE_NAME = "healthupdate"
    }

    stages {

        stage('📥 Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('🐍 Setup Python Virtualenv') {
            steps {
                sh '''
                    python3 -m venv venv

                    venv/bin/python -m pip install --upgrade pip
                    venv/bin/python -m pip install -r requirements.txt

                    # Dev tools
                    venv/bin/python -m pip install flake8
                '''
            }
        }

        stage('🔍 Run Lint') {
            steps {
                sh '''
                    venv/bin/python -m flake8 . \
                        --max-line-length=120 \
                        --exclude=venv,migrations,__pycache__,.git
                '''
            }
        }

        stage('🧪 Run Django Tests') {
            steps {
                sh '''
                    venv/bin/python manage.py test
                '''
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                sh '''
                    docker pull python:3.11-slim || true
                    docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }
    }

    post {
        success {
            echo """
=========================
✅ CI PIPELINE SUCCESS
=========================
✔ Checkout
✔ Python Setup
✔ Lint Passed
✔ Tests Passed
✔ Docker Build Passed
=========================
"""
        }

        failure {
            echo """
=========================
❌ CI PIPELINE FAILED
=========================
Check:
- Lint errors
- Test failures
- Docker build issues
=========================
"""
        }

        always {
            cleanWs()
        }
    }
}