pipeline {
    agent any

    environment {
        IMAGE_NAME = "django_health_app"
        SONARQUBE_SERVER = "SonarQube"
        SLACK_CHANNEL = "#jenkins-alerts"
    }

    options {
        timestamps()
        skipStagesAfterUnstable()
    }

    stages {

        stage('📥 Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('🔍 Code Analysis (SonarQube)') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh '''
                    docker run --rm \
                      --network sonarqube_default \
                      -v ${WORKSPACE}:/usr/src \
                      sonarsource/sonar-scanner-cli \
                      -Dsonar.projectKey=django_health_app \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=http://sonarqube:9000
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

        stage('🐳 Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('🚀 Deploy (Docker Compose)') {
            steps {
                sh '''
                docker compose down --remove-orphans || true
                docker compose up -d --build --force-recreate
                '''
            }
        }

        stage('🧪 Health Check') {
            steps {
                sh '''
                sleep 10
                curl -f http://localhost:8021
                '''
            }
        }
    }

    post {
        always {
            script {
                def status = currentBuild.currentResult
                def color = (status == 'SUCCESS') ? 'good' : 'danger'

                slackSend(
                    channel: SLACK_CHANNEL,
                    color: color,
                    message: """
*CI Pipeline Result*
*Job:* ${env.JOB_NAME}
*Build:* #${env.BUILD_NUMBER}
*Status:* ${status}
*URL:* ${env.BUILD_URL}
"""
                )
            }

            sh '''
            docker ps -a
            docker images
            '''
        }
    }
}