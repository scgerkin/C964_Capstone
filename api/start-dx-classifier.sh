#!/bin/bash

sudo service docker start
sudo /usr/local/bin/docker-compose -f /home/ec2-user/docker-compose.yaml up -d
