import sys
import os
import json
import time
import requests
from typing import Dict
from datetime import datetime

HOST_AND_REPORT_DIR = "/tmp/SSLLab_hosts_and_report/Reports/"

SSLAB_API_URL = "https://api.ssllabs.com/api/v3/analyze"

SECURITY_PROTOCOLS = [
    "SSL 2.0 INSECURE", "SSL 3.0 INSECURE", "TLS 1.0", "TLS 1.1", "TLS 1.2", "TLS 1.3",       
]

SUMMARY_COLUMNS = [
    "Host", "HasWarnings", "Grade", "Cert Expiry", "Chain Status", "Forward Secrecy", "Heartbeat ext",
    "Support RC4", "RC4 Only", "RC4 with modern protocols", "Vuln Drown", "Vuln FREAK", "Vuln Beast",
    "Vuln Heartbleed", "Vuln POODLE", "Vuln POODLE TLS", "Vuln openSsl Ccs", "Vuln openSSL LuckyMinus20",
] + SECURITY_PROTOCOLS

SSLLAB_CHAIN_ISSUES = {
    "0": "none",
    "1": "unused",
    "2": "incomplete chain (set only when we were able to build a chain by adding missing intermediate certificates from external sources)",
    "4": "chain contains unrelated or duplicate certificates (i.e., certificates that are not part of the same chain)",
    "8": "the certificates form a chain (trusted or not), but the order is incorrect",
    "16": "contains a self-signed root certificate (not set for self-signed leafs)",
    "32": "the certificates form a chain that we could not validate",
}

SSLLAB_FORWARD_SECRECY = {
    "1": "at least one browser from our simulations negotiated a Forward Secrecy suite",
    "2": "FS is achieved with modern clients",
    "4": "all simulated clients achieved FS",
}

def get_ssllab_scan_results(host: str, csv_summary_file: str, number_of_attempts: int=20):
    
    ssllab_request_params = get_ssllab_request_params(host)
    sslab_scan_results = execute_api_url(ssllab_request_params, number_of_attempts) 
    ssllab_request_params.pop("startNew")
    print(csv_summary_file)

    while sslab_scan_results["status"] != "READY" and sslab_scan_results["status"] != "ERROR":
        time.sleep(10)
        sslab_scan_results = execute_api_url(ssllab_request_params, number_of_attempts)

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
    api_response = requests.get(SSLAB_API_URL, params=ssllab_request_params)
    attempts = 0 
    while api_response.status_code != 200 and attempts < number_of_attempts:
        attempts += 1
        time.sleep(10)
        api_response = requests.get(SSLAB_API_URL, params=ssllab_request_params)
    return api_response.json()

def summary_csv_append(host, sslab_data, csv_summary_file):
    try:
        with open(csv_summary_file, "a") as output_file:
            not_after = sslab_data["certs"][0]["notAfter"]
            not_after = float(str(not_after)[:10])
            not_after_date = datetime.utcfromtimestamp(not_after).strftime("%Y-%m-%d")

            for endpoint in sslab_data["endpoints"]:
               # Endpoints to be ingored which could not be scanned
               if "Unable" in endpoint["statusMessage"]:
                   continue

               summary_csv = [
                   host,
                   endpoint["hasWarnings"],
                   endpoint["grade"],
                   not_after_date,
                   SSLLAB_CHAIN_ISSUES[str(endpoint["details"]["certChains"][0]["issues"])],
                   SSLLAB_FORWARD_SECRECY[str(endpoint["details"]["forwardSecrecy"])],
                   endpoint["details"]["heartbeat"],
                   endpoint["details"]["supportsRc4"],
                   endpoint["details"]["rc4Only"],
                   endpoint["details"]["rc4WithModern"],
                   endpoint["details"]["drownVulnerable"],
                   endpoint["details"]["freak"],
                   endpoint["details"]["vulnBeast"],
                   endpoint["details"]["heartbleed"],
                   endpoint["details"]["poodle"],
                   False if endpoint["details"]["poodleTls"] == 1 else True,
                   False if endpoint["details"]["openSslCcs"] == 1 else True,
                   False if endpoint["details"]["openSSLLuckyMinus20"] == 1 else True,
               ]
               for protocol in SECURITY_PROTOCOLS:
                   found = False
                   for endpoint_protocol in endpoint["details"]["protocols"]:
                       endpoint_protocol_name = f"{endpoint_protocol['name']} {endpoint_protocol['version']}"
                       if protocol == endpoint_protocol_name:
                           found = True
                           break
                   if found:
                       summary_csv += ["Yes"]
                   else:
                       summary_csv += ["No"]

            output_file.write(",".join(str(s) for s in summary_csv) + "\n")
    except Exception as err:
       print(f"ERROR: SSLLabs report for domain {host} could not be added to csv due to Error:\n {err}")
