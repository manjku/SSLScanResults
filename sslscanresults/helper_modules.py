import sys
import os
import json
import time
import requests
from typing import Dict
from datetime import datetime

HOST_AND_REPORT_DIR = "/tmp/SSLLab_hosts_and_report/Reports/"

api_url = "https://api.ssllabs.com/api/v3/analyze"

CHAIN_ISSUES = {
    "0": "none",
    "1": "unused",
    "2": "incomplete chain",
    "4": "chain contains unrelated or duplicate certificates",
    "8": "the certificates form a chain (trusted or not) but incorrect order",
    "16": "contains a self-signed root certificate",
    "32": "the certificates form a chain but cannot be validated",
}

# Forward secrecy protects past sessions against future compromises of secret keys or passwords.
FORWARD_SECRECY = {
    "1": "With some browsers WEAK",
    "2": "With modern browsers",
    "4": "Yes (with most browsers) ROBUST",
}

SECURITY_PROTOCOLS = [
    "SSL 2.0 INSECURE", "SSL 3.0 INSECURE", "TLS 1.0", "TLS 1.1", "TLS 1.2", "TLS 1.3",       
]

RC4 = ["Support RC4", "RC4 with modern protocols", "RC4 Only"]

VULNERABLES = [
    "Vuln Beast", "Vuln Drown", "Vuln Heartbleed", "Vuln FREAK",
    "Vuln openSsl Ccs", "Vuln openSSL LuckyMinus20", "Vuln POODLE", "Vuln POODLE TLS"
]

SUMMARY_COLUMNS = [
    "Host", "HasWarnings", "Grade", "Cert Expiry", "Chain Status", "Forward Secrecy", "Heartbeat ext"
] + VULNERABLES + RC4 + SECURITY_PROTOCOLS

def get_ssllab_scan_results(host: str, csv_summary_file: str, number_of_attempts: int=20):
    
    ssllab_request_params = get_ssllab_request_params(host)
    sslab_scan_results = execute_api_url(ssllab_request_params, number_of_attempts) 
    ssllab_request_params.pop("startNew")
    print(csv_summary_file)

    while sslab_scan_results["status"] != "READY" and sslab_scan_results["status"] != "ERROR":
        print(f"Status: {sslab_scan_results['status']}, wait for 10 seconds...")
        time.sleep(10)
        sslab_scan_results = execute_api_url(ssllab_request_params, number_of_attempts)
        print(f"Status before while loop : {sslab_scan_results['status']}")

    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    json_output_file = os.path.join(os.path.dirname(HOST_AND_REPORT_DIR),"json_reports",f"{host}.json_{date}")

    with open(json_output_file, "w") as outputfile:
        json.dump(sslab_scan_results, outputfile, indent=2)

    summary_csv_append(host, sslab_scan_results, csv_summary_file)

    return sslab_scan_results

def get_ssllab_request_params(host: str):
    params = {
        "host": host,
        "ignoreMismatch":"on",
        "all":"done",
        "publish":"off",
        "startNew":"off",
    }
    return params
    
def execute_api_url(ssllab_request_params, number_of_attempts):
    api_response = requests.get(api_url, params=ssllab_request_params)
    attempts = 0 
    while api_response.status_code != 200 and attempts < number_of_attempts:
        print(f"Response code: {str(api_response.status_code)} - Error on requesting API. "
              f"Waiting for 10 sec until next retry...")
        attempts += 1
        time.sleep(10)
        api_response = requests.get(api_url, params=ssllab_request_params)
    return api_response.json()

def summary_csv_append(host, sslab_data, csv_summary_file):
    with open(csv_summary_file, "a") as output_file:
        not_after = sslab_data["certs"][0]["notAfter"]
        not_after_date = time.strftime("%D", time.localtime(int(not_after)))
        for endpoint in sslab_data["endpoints"]:
           # Endpoints to be ingored which could not be scanned
           if "Unable" in endpoint["statusMessage"]:
               continue

           summary_csv = [
               host,
               endpoint["hasWarnings"],
               endpoint["grade"],
               not_after_date,
               CHAIN_ISSUES[str(endpoint["details"]["certChains"][0]["issues"])],
               FORWARD_SECRECY[str(endpoint["details"]["forwardSecrecy"])],
               endpoint["details"]["heartbeat"],
               endpoint["details"]["vulnBeast"],
               endpoint["details"]["drownVulnerable"],
               endpoint["details"]["heartbleed"],
               endpoint["details"]["freak"],
               False if endpoint["details"]["openSslCcs"] == 1 else True,
               False if endpoint["details"]["openSSLLuckyMinus20"] == 1 else True,
               endpoint["details"]["poodle"],
               False if endpoint["details"]["poodleTls"] == 1 else True,
               endpoint["details"]["supportsRc4"],
               endpoint["details"]["rc4WithModern"],
               endpoint["details"]["rc4Only"],
           ]
           for protocol in SECURITY_PROTOCOLS:
               found = False
               for endpoint_protocol in endpoint["details"]["protocols"]:
                   endpoint_protocol_name = f"{endpoint_protocol['name']} {endpoint_protocol['version']}"
                   print(f"endpoint_protocol_name is {endpoint_protocol_name}")
                   if protocol == endpoint_protocol_name:
                       found = True
                       break
               if found:
                   summary_csv += ["Yes"]
               else:
                   summary_csv += ["No"]

        output_file.write(",".join(str(s) for s in summary_csv) + "\n")
