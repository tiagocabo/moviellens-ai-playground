# moviellens-ai-playground
Experimenting recommendations systems with movilens dataset

# Data

### Movielens-100k
In order to download run:
```
curl -o movielens_100k.zip https://files.grouplens.org/datasets/movielens/ml-100k.zip

# To unzip 
unzip movielens_100k.zip
```

Poster data collected from here https://github.com/tiagocabo/movielens-posters/blob/master/README.md

### How to deploy on aws
1- Follow instructions in the UI
2- Create default VPC, don't forget to expose the custom port used in the streamlit
3- download key, and change permission using `chmod 600 pem file`
4- log into the machine following aws instructions
5- install docker and make using https://cloudaffaire.com/how-to-install-docker-in-aws-ec2-instance/
6- run make lunch
7- After, don't forget to use http in the url and to add the exposed port.