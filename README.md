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
