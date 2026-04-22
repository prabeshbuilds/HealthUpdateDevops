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
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install flake8 coverage
                '''
            }
        }

        stage('🔍 Lint Code') {
            steps {
                sh '''
                    . venv/bin/activate

                    flake8 . \
                        --max-line-length=120 \
                        --exclude=venv,migrations,__pycache__,.git
                '''
            }
        }

        stage('🧪 Run Tests & Coverage') {
            steps {
                sh '''
                    . venv/bin/activate

                    coverage run manage.py test
                    coverage report
                    coverage xml -o coverage.xml

                    ls -la coverage.xml
                '''
            }
        }

        stage('📊 SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=health-update-app \
                            -Dsonar.projectName="Health Update App" \
                            -Dsonar.sources=. \
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

        stage('🐳 Docker Build') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:latest .

                    echo "Docker Images:"
                    docker images | grep ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        success {
            echo """
==============================
✅ PIPELINE SUCCESS
==============================
✔ Checkout
✔ Python Setup
✔ Lint Passed
✔ Tests Passed
✔ Coverage Generated
✔ SonarQube Passed
✔ Quality Gate Passed
✔ Docker Build Success
==============================
"""
        }

        failure {
            echo """
==============================
❌ PIPELINE FAILED
==============================
Check logs for:
- Lint errors
- Test failures
- SonarQube issues
- Docker build errors
==============================
"""
        }

        always {
            cleanWs()
        }
    }
}