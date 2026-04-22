pipeline {
    agent any

    environment {
        IMAGE_NAME = "HealthUpdateApp"
    }

    stages {

        stage('📥 Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/prabeshbuilds/HealthUpdateDevops.git'
            }
        }

        stage('🐍 Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    # Dev tools
                    pip install flake8 pytest pytest-django coverage
                '''
            }
        }

        // ✅ CODE QUALITY (Lint)
        stage('🔍 Code Quality - Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    echo "Running flake8..."
                    flake8 . --max-line-length=120
                '''
            }
        }

        // ✅ TEST + COVERAGE (IMPORTANT for Sonar)
        stage('🧪 Tests with Coverage') {
            steps {
                sh '''
                    . venv/bin/activate
                    coverage run manage.py test
                    coverage xml
                '''
            }
        }

        // ✅ SONARQUBE ANALYSIS (Correct way)
        stage('📊 SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=todo-django \
                          -Dsonar.projectName=todo-django \
                          -Dsonar.sources=. \
                          -Dsonar.python.coverage.reportPaths=coverage.xml \
                          -Dsonar.exclusions=venv/**,migrations/**,static/**
                    '''
                }
            }
        }

        // ✅ QUALITY GATE
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
                '''
            }
        }
    }

    post {
        success {
            echo '''
✅ CI SUCCESS
✔ Lint Passed
✔ Tests Passed
✔ Quality Gate Passed
✔ Docker Build Passed
'''
        }
        failure {
            echo '''
❌ CI FAILED
Check:
- Lint errors
- Test failures
- Sonar Quality Gate
'''
        }
        always {
            cleanWs()
        }
    }
}