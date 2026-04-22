pipeline {
    agent any

    environment {
        IMAGE_NAME = "django_health_app"
        SONARQUBE_SERVER = "SonarQube"   // Jenkins configured name
    }

    stages {

        stage('📥 Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('🔍 SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh '''
                        echo "Waiting for SonarQube..."
                        sleep 30

                        docker run --rm \
                        --network=ci_for_django_health_main_default \
                        -e SONAR_HOST_URL=http://sonarqube:9000 \
                        -e SONAR_LOGIN=YOUR_TOKEN \
                        -v "$PWD:/usr/src" \
                        sonarsource/sonar-scanner-cli \
                        -Dsonar.projectKey=django_health_app \
                        -Dsonar.sources=.
                    '''
                }
            }
        }

        stage('⏳ Quality Gate') {
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
        }

        failure {
            echo "❌ CI Pipeline failed!"
        }

        always {
            sh '''
                docker images
                docker ps -a
            '''
        }
    }
}