pipeline {
    agent any

    tools {
        sonarScanner 'SonarScanner'
    }

    environment {
        IMAGE_NAME = "django_health_app"
    }

    stages {

        stage('📥 Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        // 🔍 SonarQube Analysis
        stage('🔍 SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=django-health-app \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=$SONAR_HOST_URL
                    '''
                }
            }
        }

        // 🚦 Quality Gate (WAIT FOR WEBHOOK)
        stage('🚦 Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('🐳 Clean Old Containers') {
            steps {
                sh '''
                    docker compose down --remove-orphans || true
                    docker rm -f django_health_app || true
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

        stage('🚀 Run Containers') {
            steps {
                sh '''
                    docker compose up -d --build --force-recreate
                '''
            }
        }

        stage('🧪 Health Check') {
            steps {
                sh '''
                    sleep 5
                    docker ps
                    curl -f http://localhost:8021 || true
                '''
            }
        }
    }

    post {

        success {
            echo "✅ CI Pipeline completed successfully!"

            slackSend (
                channel: 'test',
                color: 'good',
                message: "✅ SUCCESS: Django Health App deployed successfully.\nJob: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }

        failure {
            echo "❌ CI Pipeline failed!"

            slackSend (
                channel: 'test',
                color: 'danger',
                message: "❌ FAILED: Django Health App pipeline failed.\nJob: ${env.JOB_NAME} #${env.BUILD_NUMBER}\nCheck Jenkins logs."
            )
        }

        always {
            sh '''
                docker images
                docker ps -a
            '''

            slackSend (
                channel: 'alert',
                color: '#439FE0',
                message: "ℹ️ Jenkins job finished: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}