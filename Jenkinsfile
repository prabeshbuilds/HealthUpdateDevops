pipeline {
    agent any

    environment {
        IMAGE_NAME = "health-update-app"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {
        stage('📥 Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('🐍 Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install --upgrade pip
                    venv/bin/pip install -r requirements.txt
                    venv/bin/pip install flake8 coverage
                '''
            }
        }

        stage('🔍 Code Quality (Lint)') {
            steps {
                sh 'venv/bin/flake8 . --max-line-length=120 --exclude=venv,migrations,__pycache__'
            }
        }

        stage('🧪 Tests + Coverage') {
            steps {
                sh '''
                    venv/bin/coverage run manage.py test
                    venv/bin/coverage xml
                '''
            }
        }

        stage('📊 SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=health-update-app \
                            "-Dsonar.projectName=Health Update App" \
                            -Dsonar.sources=. \
                            -Dsonar.language=py \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.exclusions=venv/**,**/migrations/**,**/__pycache__/**
                    '''
                }
            }
        }

        stage('🚦 Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:latest .
                    docker images | grep ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        success {
            echo '''
==============================
✅ CI PIPELINE SUCCESS
==============================
✔ Code Checkout OK
✔ Lint Passed
✔ Tests Passed
✔ Sonar Quality Gate Passed
✔ Docker Build Successful
==============================
'''
        }
        failure {
            echo '''
==============================
❌ CI PIPELINE FAILED
==============================
Check:
- Lint errors
- Test failures
- SonarQube Quality Gate
- Docker build logs
==============================
'''
        }
        always {
            cleanWs()
        }
    }
}