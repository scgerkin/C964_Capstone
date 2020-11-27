#!/bin/bash

# Installs up docker and docker-compose, gets the containers from ECR, and starts the service.
yum update -y
yum install docker -y
service docker start
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 854235326474.dkr.ecr.us-east-1.amazonaws.com
sudo docker pull 854235326474.dkr.ecr.us-east-1.amazonaws.com/c964/dx:latest
sudo docker pull 854235326474.dkr.ecr.us-east-1.amazonaws.com/c964/svr:latest
docker image tag 854235326474.dkr.ecr.us-east-1.amazonaws.com/c964/svr c964/svr
docker image tag 854235326474.dkr.ecr.us-east-1.amazonaws.com/c964/dx c964/dx
curl https://raw.githubusercontent.com/scgerkin/C964_Capstone/main/ml/api/docker-compose.yaml > /home/ec2-user/docker-compose.yaml
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
/usr/local/bin/docker-compose -f /home/ec2-user/docker-compose.yaml up -d
