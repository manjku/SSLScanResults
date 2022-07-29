# Pull base image.
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3.6
RUN apt install -y python3-pip
WORKDIR /tmp
RUN git clone https://github.com/manjku/SSLLab_hosts_and_report.git
WORKDIR /project
RUN git clone https://github.com/manjku/SSLScanResults.git
RUN pip3 install -r SSLScanResults/requirements.txt
CMD SSLScanResults/sslscanresults/sslscan-results.py
