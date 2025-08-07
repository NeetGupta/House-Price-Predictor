pipeline {
    agent{
        docker {
            image 'python:3.10'
        }
    }
    environment {
        IMAGE_NAME = 'yourdockerhubusername/flask-ml-api'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/NeetGupta/House-Price-Predictor.git', branch: 'main', credentialsId: 'Github-ID'
            }
        }

        stage('Install Requirements') {
            steps {
             sh '''
            python3 -m venv venv
            . venv/bin/activate
            pip install --upgrade pip
            pip install -r app/requirements.txt
        '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest tests/test_app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $IMAGE_NAME
                    '''
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                sshagent(['ssh-ec2-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ec2-user@your-ec2-ip "
                        docker pull $IMAGE_NAME &&
                        docker stop mlapi || true &&
                        docker rm mlapi || true &&
                        docker run -d --name mlapi -p 80:5000 $IMAGE_NAME
                    "
                    '''
                }
            }
        }
    }
}
