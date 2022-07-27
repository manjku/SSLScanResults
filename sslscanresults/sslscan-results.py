#!/usr/bin/python3
import os
import sys
import csv
from helper_modules import get_ssllab_scan_results

def main():
    data = get_ssllab_scan_results("google.com")
    print(data)

if __name__ == "__main__":
    sys.exit(main())
