import sys
import os
import json
import time
import requests
from typing import Dict

api_url = "https://api.ssllabs.com/api/v3/analyze"
def get_ssllab_scan_results(host: str, number_of_attempts: int=20):
    
    ssllab_request_params = get_ssllab_request_params(host)
    sslab_scan_results = execute_api_url(ssllab_request_params, number_of_attempts) 
    ssllab_request_params.pop("startNew")
    print(f"ssllab_request_params: {str(ssllab_request_params)}")

    while sslab_scan_results["status"] != "READY" and sslab_scan_results["status"] != "ERROR":
        print(f"Status: {sslab_scan_results['status']}, wait for 10 seconds...")
        time.sleep(10)
        sslab_scan_results = execute_api_url(ssllab_request_params, number_of_attempts)
        print(f"Status before while loop : {sslab_scan_results['status']}")
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
    
