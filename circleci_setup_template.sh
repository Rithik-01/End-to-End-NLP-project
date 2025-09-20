# Setup Docker and update system
sudo apt-get update
sudo apt-get upgrade -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh



# Add cloud user to docker group
sudo usermod -aG docker ubuntu
sudo usermod -aG docker $USER
newgrp docker



# Start configuration of self-hosted machine
# Download the launch agent binary and verify the checksum
mkdir configurations
cd configurations
curl https://raw.githubusercontent.com/CircleCI-Public/runner-installation-files/main/download-launch-agent.sh > download-launch-agent.sh
export platform=linux/amd64 && sh ./download-launch-agent.sh



# Create the circleci user & working directory
id -u circleci &>/dev/null || sudo adduser --disabled-password --gecos GECOS circleci
sudo mkdir -p /var/opt/circleci
sudo chmod 0750 /var/opt/circleci
sudo chown -R circleci /var/opt/circleci /opt/circleci/circleci-launch-agent

# for ubuntu 24.04
sudo apt update
sudo apt install nano -y

# Create a CircleCI runner configuration
sudo mkdir -p /etc/opt/circleci
sudo touch /etc/opt/circleci/launch-agent-config.yaml
sudo nano /etc/opt/circleci/launch-agent-config.yaml



# Add API in the file and change permissions
api:
  auth_token: ed3f94b5d348a6a45f84b79fa2b1387042a3597620bb52b12c36b6a8380ad09f9be3b7f93a705553

runner:
  name: self-hosted
  working_directory: /var/opt/circleci/workdir
  cleanup_working_directory: true



sudo chown circleci: /etc/opt/circleci/launch-agent-config.yaml
sudo chmod 600 /etc/opt/circleci/launch-agent-config.yaml


# Enable the systemd unit
sudo touch /usr/lib/systemd/system/circleci.service
sudo nano /usr/lib/systemd/system/circleci.service



# Put Content in the circleci.service
[Unit]
Description=CircleCI Runner
After=network.target
[Service]
ExecStart=/opt/circleci/circleci-launch-agent --config /etc/opt/circleci/launch-agent-config.yaml
Restart=always
User=circleci
NotifyAccess=exec
TimeoutStopSec=18300
[Install]
WantedBy = multi-user.target





sudo chown root: /usr/lib/systemd/system/circleci.service
sudo chmod 644 /usr/lib/systemd/system/circleci.service




# Start CircleCI
sudo systemctl enable circleci.service
sudo systemctl start circleci.service




## Add circleci to sudo group
sudo usermod -aG docker circleci
sudo usermod -a -G docker circleci
newgrp docker


sudo systemctl status circleci.service



# Install Googlecli
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates gnupg curl
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg |  sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

