# Create virtual environment:
pip3 install virtualenv
mkdir project_A
cd project_A
virtualenv my_new_venv
source my_new_venv/bin/activate

# Clone the project repo and install dependency packages from requirements.txt : 
git clone https://github.com/manjku/SSLScanResults.git
pip3 install -r SSLScanResults/requirements.txt

# Execute the script:
python3 SSLScanResults/sslscanresults/sslscan-results.py


#####  Execute tool in a docker instance #####
git clone https://github.com/manjku/SSLScanResults.git
cd SSLScanResults
docker build -t ssllab_report:21.0 . 

# Get the docker image ID:

docker images ssllab_report:21.0
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
ssllab_report   21.0      00528c8085e4   37 seconds ago   677MB

# Create docker container to execute the tool 
docker run 00528c8085e4
