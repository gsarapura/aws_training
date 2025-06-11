# Using an EC2 Instance with abctl
https://docs.airbyte.com/platform/deploying-airbyte/abctl-ec2

## Suggested resources
For best performance, run Airbyte on a machine with 4 or more CPUs and at least 8-GB of memory. Airbyte also runs with 2 CPUs and 8-GB of memory in low-resource mode. This guide explains how to do both. Follow this Github discussion to up-vote and track progress toward supporting lower resource environments.

## Installation
```bash
#####################################
sudo dnf update
sudo yum install -y docker
sudo usermod -a -G docker ec2-user
sudo systemctl start docker
sudo systemctl enable docke
# To run docker as non-root
exit
ssh -i ec2-user-key.pem ec2-user@1.2.3.4

# Install abctl
curl -LsfS https://get.airbyte.com | bash -

#####################################

# Prod? Nginx + Certbot to enable https
abctl local install 
# For testing
abctl local install --low-resource-mode
abctl local install --host $HOST
abctl local install --host $HOST --insecure-cookies

```

## Enable HTTPS
```bash
# Nginx
sudo dnf install nginx

sudo systemctl enable nginx && sudo systemctl start nginx

sudo vim /etc/nginx/nginx.conf
: '
I decided to remove the default file in site-enabled (following meilisearch), but, at least in Amazon Linux 2023, I had to remove the server{} config for port 80 in nginx.conf and added:

# Add this line to include sites-enabled
include /etc/nginx/sites-enabled/*;
'
sudo vim /etc/nginx/site-enabled/airbyte

# When running cerbot, cerbot will add conf for 443
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    client_max_body_size 200M;  # required for Airbyte API

    location / {
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Cookie $http_cookie;  # if you use Airbyte's basic auth
      proxy_read_timeout 3600;  # set a number in seconds suitable for you
      proxy_pass  http://localhost:8000;
    }
}

# Install cerbot
sudo yum install epel-release
sudo yum install certbot-nginx

# Follow prompt to add domain
sudo certbot --nginx 
# Renew
sudo certbot renew 

# Test renew
sudo certbot renew --dry-run

# Port 80 needs to be opened for cerbot to renew?
```