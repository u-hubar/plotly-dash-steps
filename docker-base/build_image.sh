sudo docker build -f Dockerfile-base -t dash_app_base:latest .
sudo docker save dash_app_base:latest > dash_app_base.tar