pipeline {
    agent any

    environment {
        IMAGE_NAME = "django_health_app"
        CONTAINER_NAME = "django_health_app"
    }

    stages {

        stage('📥 Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('🐳 Stop Old Containers') {
            steps {
                sh '''
                    docker compose down || true
                '''
            }
        }

        stage('🏗️ Build Docker Image') {
            steps {
                sh '''
                    docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('🚀 Run Docker Compose') {
            steps {
                sh '''
                    docker compose up -d --build
                '''
            }
        }

    }

    post {
        success {
            echo "✅ CI Pipeline completed successfully!"
        }

        failure {
            echo "❌ CI Pipeline failed!"
        }

        always {
            sh '''
                docker images
                docker ps
            '''
        }
    }
}