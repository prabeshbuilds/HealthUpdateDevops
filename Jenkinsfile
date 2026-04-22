pipeline {
    agent any

    environment {
        IMAGE_NAME = "healthupdat"
        VENV = "venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('Create Virtual Environment & Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    $VENV/bin/pip install --upgrade pip
                    $VENV/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Lint (flake8)') {
            steps {
                sh '''
                    $VENV/bin/pip install flake8
                    $VENV/bin/flake8 . || true
                '''
            }
        }

        stage('Run Django Tests') {
            steps {
                sh '''
                    $VENV/bin/python manage.py test
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

        stage('Run Docker Container (Optional Test)') {
            steps {
                sh '''
                    docker run -d --name healthapp_test -p 8000:8000 $IMAGE_NAME:latest || true
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
            sh '''
                docker rm -f healthapp_test || true
            '''
            cleanWs()
        }
    }
}