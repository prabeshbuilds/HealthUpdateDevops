pipeline {
    agent any

    environment {
        APP_NAME        = "django_health_app"
        SONAR_SERVER    = "SonarQube"
        SLACK_CHANNEL   = "#jenkins-alerts"
        APP_URL         = "http://localhost:8021"
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
                notifySlack(currentBuild.currentResult)
            }

            sh """
            docker ps -a
            docker images
            """
        }
    }
}

def notifySlack(status) {
    def colorMap = [
        'SUCCESS': 'good',
        'FAILURE': 'danger',
        'UNSTABLE': 'warning'
    ]

    slackSend(
        channel: SLACK_CHANNEL,
        color: colorMap.get(status, 'danger'),
        message: """
            *CI Result:* ${status}
            *Job:* ${env.JOB_NAME}
            *Build:* #${env.BUILD_NUMBER}
            *URL:* ${env.BUILD_URL}
            """
    )
}