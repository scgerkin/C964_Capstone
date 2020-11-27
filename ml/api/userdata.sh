#!/bin/bash

# Installs up docker and docker-compose, gets the containers from ECR, and starts the service.
yum update -y
yum install docker -y
service docker start
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 854235326474.dkr.ecr.us-east-1.amazonaws.com
docker pull 854235326474.dkr.ecr.us-east-1.amazonaws.com/c964/dx:latest
docker pull 854235326474.dkr.ecr.us-east-1.amazonaws.com/c964/svr:latest
docker image tag 854235326474.dkr.ecr.us-east-1.amazonaws.com/c964/svr c964/svr
docker image tag 854235326474.dkr.ecr.us-east-1.amazonaws.com/c964/dx c964/dx
curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/ml/api/docker-compose.yaml > /home/ec2-user/docker-compose.yaml
curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/ml/api/dx-classifier.service > /home/ec2-user/dx-classifier.service
curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/ml/api/start-dx-classifier.sh > /home/ec2-user/start-dx-classifier.sh
chmod +x /home/ec2-user/start-dx-classifier.sh
systemctl enable /home/ec2-user/dx-classifier.service
systemctl start dx-classifier
