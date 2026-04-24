pipeline {
    agent any

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
                        docker run --rm \
                        -v "$PWD:/usr/src" \
                        sonarsource/sonar-scanner-cli \
                        -Dsonar.projectKey=django-health-app \
                        -Dsonar.projectName=django-health-app \
                        -Dsonar.sources=/usr/src \
                        -Dsonar.host.url=https://b370-2405-acc0-1207-c28b-6fe7-6ca0-5f1-ec2f.ngrok-free.app \
                        -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('🚦 Quality Gate') {
            steps {
                echo "⚠️ Skipping Quality Gate because Docker scanner does not support Jenkins taskId tracking"
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
                sh """
                    docker rm -f ${CONTAINER_NAME} || true

                    docker run -d \
                    --name ${CONTAINER_NAME} \
                    -p 8021:8000 \
                    ${IMAGE_NAME}
                """
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
            slackSend channel: 'test', color: 'good',
                message: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }

        failure {
            echo "❌ Pipeline FAILED"
            slackSend channel: 'test', color: 'danger',
                message: "❌ FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }

        always {
            sh '''
                docker ps -a
                docker images
            '''
        }
    }
}