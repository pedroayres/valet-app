# How to run project
- crossbar start (on server_side)
- gunicron app:app (on server_side)
- ionic serve(on client_side)

# Dependecies
easy_install pip
pip install crossbar[all]
pip install crossbar --upgrade
pip install falcon
pip install --upgrade cython falcon
pip install gunicorn
pip install service-identity

# Only for Linux
sudo yum install libffi-devel 

# Ubuntu
sudo apt-get install python-pip python-dev build-essential 
sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-pip

# Only for MAC
xcode-select --install

# Upload to Mobile
ionic upload
