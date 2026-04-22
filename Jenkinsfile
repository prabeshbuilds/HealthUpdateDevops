pipeline {
    agent any

    environment {
        APP_NAME     = "django_health_app"
        SONAR_SERVER = "SonarQube"
        APP_URL      = "http://localhost:8021"
    }

    options {
        timestamps()
        skipStagesAfterUnstable()
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(SONAR_SERVER) {
                    sh """
                    docker run --rm \
                      --network sonarqube_default \
                      -v ${WORKSPACE}:/usr/src \
                      sonarsource/sonar-scanner-cli \
                      -Dsonar.projectKey=${APP_NAME} \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=http://sonarqube:9000
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Image') {
            steps {
                sh "docker build -t ${APP_NAME} ."
            }
        }

        stage('Deploy') {
            steps {
                sh """
                docker compose down --remove-orphans || true
                docker compose up -d --build --force-recreate
                """
            }
        }

        stage('Health Check') {
            steps {
                sh """
                sleep 10
                curl -f ${APP_URL}
                """
            }
        }
    }

    post {
        always {
            script {
                slackSend(
                    color: currentBuild.currentResult == 'SUCCESS' ? 'good' : 'danger',
                    message: """
*CI RESULT:* ${currentBuild.currentResult}
*Job:* ${env.JOB_NAME}
*Build:* #${env.BUILD_NUMBER}
*URL:* ${env.BUILD_URL}
"""
                )
            }

            sh """
            docker ps -a
            docker images
            """
        }
    }
}