# Pull base image.
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3.6
RUN apt install -y python3-pip
RUN pip3 install requests
WORKDIR /project
RUN git clone https://github.com/manjku/SSLScanResults.git
CMD SSLScanResults/sslscanresults/sslscan-results.py
