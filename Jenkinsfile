pipeline {
    agent any

    tools {
        SonarScanner 'SonarScanner'
    }

    environment {
        IMAGE_NAME = "django_health_app"
        CONTAINER_NAME = "django_health_app"
    }

    stages {

        stage('📥 Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('🔍 SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=django-health-app \
                          -Dsonar.projectName=django-health-app \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=$SONAR_HOST_URL \
                          -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('🚦 Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('🐳 Stop Old Containers') {
            steps {
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
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

        stage('🚀 Run Container') {
            steps {
                sh '''
                    docker run -d \
                      --name $CONTAINER_NAME \
                      -p 8021:8000 \
                      $IMAGE_NAME
                '''
            }
        }

        stage('🧪 Health Check') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://localhost:8021 || exit 1
                '''
            }
        }
    }

    post {

        success {
            echo "✅ Pipeline SUCCESS"

            slackSend (
                channel: 'test',
                color: 'good',
                message: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER} deployed successfully"
            )
        }

        failure {
            echo "❌ Pipeline FAILED"

            slackSend (
                channel: 'test',
                color: 'danger',
                message: "❌ FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }

        always {
            sh '''
                docker ps -a
                docker images
            '''

            slackSend (
                channel: 'alert',
                color: '#439FE0',
                message: "ℹ️ Job finished: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}