* $ docker ps 
* $ docker run hello-world 
* $ docker run postgres:latest 
* $ docker-machine ssh
* $ docker stop <container_id>
* $ docker pull postgres:latest
* $ docker run --name psql -e POSTGRES_PASSWORD=password! -p 5432:5432 -d postgres:latest
* $ docker ps
* $ psql -h 0.0.0.0 -p 5432 -U postgres
* $ docker stop <container_id>
* $ docker system prune -a

* $ vim Dockerfile
* --Ctrl+C >>> :w
* $ touch Dockerfile
* $ docker build --tag <imageName> .
* $ docker build -t test .
* $ docker run test -rm
* $ docker run  -p 80:8080 test
* $ curl http://0.0.0.0/
* $ docker images
* $ docker image rm -f <image_name>

## 

* $ aws configure list
* $ aws configure --profile default
* $ aws sts get-caller-identity
* $ aws iam create-role --role-name UdacityFlaskDeployCBKubectlRole --assume-role-policy-document file://trust.json --output text --query 'Role.Arn'
* $ aws iam put-role-policy --role-name UdacityFlaskDeployCBKubectlRole --policy-name eks-describe --policy-document file://iam-role-policy.json
* $ aws s3 ls
* $ eksctl create cluster --name eksctl-demo
* $ kubectl get nodes
* $ eksctl delete cluster eksctl-demo
* $ aws ssm put-parameter --name JWT_SECRET --value "YourJWTSecret" --type SecureString

# 

* $ pip install -r requirements.txt
* $ export JWT_SECRET='myjwtsecret'
* $ export LOG_LEVEL=DEBUG
* $ export LOG_LEVEL=INFO <<<defailt
* $ python main.py
* $ export TOKEN=`curl -d '{"email":"ward@hotmail.com","password":"1234"}' -H "Content-Type: application/json" -X POST localhost:8080/auth  | jq -r '.token'`
* $ echo $TOKEN
* $ curl --request GET 'http://127.0.0.1:8080/contents' -H "Authorization: Bearer ${TOKEN}" | jq .

## 

* $ docker build -t "jwt-api-test" .
* $ docker image ls
* $ docker image rm -f <image_name>
* $ docker run --env-file=.env_file -p 80:8080 jwt-api-test
* $ docker container ls
* $ export TOKEN=`curl -d '{"email":"ward@hotmail.com","password":"1234"}' -H "Content-Type: application/json" -X POST localhost:80/auth  | jq -r '.token'`
* $ curl --request GET 'http://127.0.0.1:80/contents' -H "Authorization: Bearer ${TOKEN}" | jq .

* - If required, you can stop a container using docker stop [OPTIONS] CONTAINER [CONTAINER...] or delete a container using docker rm [OPTIONS] CONTAINER [CONTAINER...]

## 

* -Create a Kubernetes (EKS) Cluster__(simple-jwt-api)
* $ eksctl create cluster --name simple-jwt-api
* $ kubectl get nodes
* $ aws sts get-caller-identity --query Account --output text

* $ aws iam create-role --role-name UdacityFlaskDeployCBKubectlRole --assume-role-policy-document file://trust.json --output text --query 'Role.Arn'

* $ aws iam put-role-policy --role-name UdacityFlaskDeployCBKubectlRole --policy-name eks-describe --policy-document file:///tmp/iam-role-policy

* $ kubectl get -n kube-system configmap/aws-auth -o yaml > ~/aws-auth-patch.yml
* $ kubectl patch configmap/aws-auth -n kube-system --patch "$(cat ~/aws-auth-patch.yml)"

## 

* $ kubectl get services simple-jwt-api -o wide