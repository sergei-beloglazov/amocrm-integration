import requests
import json
import os
from datetime import datetime, timedelta
from settings import token, domain, logsPath


def log_message(message):
    """Logs a message to a file with a timestamp."""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_filename = os.path.join(
        logsPath, datetime.now().strftime("%Y-%m-%d") + ".txt")
    with open(log_filename, "a") as log_file:
        log_file.write(f"{timestamp} {message}\n")


def load_leads():
    """
    Fetches leads from the AmoCRM 
    """
    function = "/api/v4/leads"
    url = f"https://{domain}{function}"
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {token}"  # Fixed incorrect header syntax
    }
    
    # Send GET request to the API
    response = requests.get(url, headers=headers)
    
    # Handle HTTP response codes
    if response.status_code == 200:
        # Success: Parse and return the response data
        data = response.json()
        log_message("Leads fetched successfully.")
        log_message(f"Response data: {data}")
        return data
    elif response.status_code == 401:
        # Unauthorized: Log and raise an exception
        log_message("Error: Unauthorized access. Please check your token.")
        raise Exception("Unauthorized access (401).")
    elif response.status_code == 402:
        # Unpaid account: Log and raise an exception
        log_message("Error: Account not paid. Please check your account status.")
        raise Exception("Account not paid (402).")
    else:
        # Unexpected response: Log and raise an exception
        log_message(f"Error: Unexpected response status code {response.status_code}.")
        raise Exception(f"Unexpected response status code {response.status_code}.")


def main():
    """
    Main function fetch leads from the AmoCRM 
    Handles exceptions and logs errors.
    """
    try:
        log_message(
            f"Fetching leads from {domain} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Fetch leads
        leads = load_leads()        
    except Exception as e:
        # Log any errors that occur
        log_message(f"Error: {str(e)}")


if __name__ == "__main__":
    main()