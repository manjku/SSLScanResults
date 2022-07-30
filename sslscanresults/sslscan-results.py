import os
import sys
import csv
import yaml
import sys
from datetime import datetime
from helper_modules import get_ssllab_scan_results, SUMMARY_COLUMNS
from csv_to_html_table import csv_to_html_table
from email_helper import send_email, RECEIVER_EMAIL
from git_helper import clone_report_repo, git_push

DOMAINS_SUMMARY_CSV = "/tmp/SSLLab_hosts_and_report/Reports/csv_reports/domains_summary.csv"
HTML_TABLE_LOCATION = "/tmp/SSLLab_hosts_and_report/Reports/html_reports/table.html"
DOMAIN_NAMES_FILE = "/tmp/SSLLab_hosts_and_report/domain_names.yaml"
def main():
    print(SUMMARY_COLUMNS)
    
    if (clone_report_repo()):
        print("Exiting as Report Repo could not be cloned")   
        return 1

    receiver_email = RECEIVER_EMAIL
    if len(sys.argv) == 2:
        receiver_email = sys.argv[1]
        print(f"SSLabs summary report Email would be sent to : [{receiver_email}]")
    else:
        print(f"Receiver email addres not provided. SSLLabs summary email would be send to defaul [manoj.cis@gmail.com]")

    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    domain_summary_csv_with_date = f"{DOMAINS_SUMMARY_CSV}_{date}" 
    html_table_location_with_date = f"{HTML_TABLE_LOCATION}_{date}"

    with open(domain_summary_csv_with_date, "w") as output_file:
        # write column names to the file
        output_file.write("{}\n".format(",".join(SUMMARY_COLUMNS)))
   
    with open(DOMAIN_NAMES_FILE) as file_data:
       domain_names_list = yaml.load(file_data, Loader=yaml.FullLoader)

    print(f"hosts are {domain_names_list}")
    for host in domain_names_list:
        data = get_ssllab_scan_results(host, domain_summary_csv_with_date)

    csv_to_html_table(domain_summary_csv_with_date, html_table_location_with_date)
    send_email(html_table_location_with_date, receiver_email=receiver_email)
    
    if (git_push()):
        print("Exiting as Report Repo could not be Pushed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
