
## Docker Moloch container

Image is based on the [ubuntu](https://registry.hub.docker.com/u/ubuntu/) base image  
Designed to get up and running quickly. Loads the viewer by default allowing you to parse large PCAPS within minutes.  
## Built on the excellent work of these 3 projects

https://github.com/MathieM/docker-moloch  
https://github.com/MathieM/docker-compose-moloch  
https://github.com/danielguerra69  

## Quick Start - Linux
Step 0 Prerequisites. Install Docker // Docker Compose // Configure Kernel
```
#Install Docker
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh

#Install Docker Compose
sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

#Increase Max Map Count for Elastic Search
sysctl -w vm.max_map_count=262144
```
1. Clone the repository
```
git clone https://github.com/piesecurity/docker-moloch.git
cd ./docker-moloch
```
2. Change this line in docker-compose.yml
```
MOLOCH_PASSWORD=PASSWORDCHANGEME
```
3. Bring up the Moloch Viewer
```
sudo docker-compose up
```
4. Visit http://127.0.0.1:8005 with your favorite web browser  
username: admin  
password: Defined in Step #2  

## Importing PCAPs
1. Place all PCAPs in the folder ./tcpdump
2. Run the following command with the container running
```
docker exec docker-moloch_moloch_1 moloch-parse-pcap-folder.sh

```
## Running

### Keep ElasticSearch Persistant
Change this line in docker-compose.yml from 'true' to 'false'
```
INITALIZEDB=
```

### Wipe your ElasticSearch DB but keep all your users and configs
Run the following command with the container running
```
docker exec docker-moloch_moloch_1 wipemoloch.sh

```
### Configure ElasticSearch to wipe each startup but keep your users and configs
Change this line in docker-compose.yml from 'true' to 'false'
```
INITALIZEDB=
```
Change this line in docker-compose.yml from 'true' to 'false'
```
WIPEDB=
```
