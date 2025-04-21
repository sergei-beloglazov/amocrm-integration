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


def load_leads(date):
    """
    Fetches leads from the AmoCRM for a specific date based on created_at.

    Parameters:
        date (str): Date in the format 'Y-m-d' to filter leads by creation date.
    """
    function = "/api/v4/leads"
    url = f"https://{domain}{function}"
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    
    # Convert the date to a timestamp range for filtering
    start_of_day = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
    end_of_day = start_of_day + 86400  # Add 24 hours to get the end of the day
    
    # Add filter parameters to the URL
    params = {
        "filter[created_at][from]": start_of_day,
        "filter[created_at][to]": end_of_day
    }
    
    # Send GET request to the API
    response = requests.get(url, headers=headers, params=params)
    
    # Handle HTTP response codes
    if response.status_code == 200:
        # Success: Parse and return the response data
        data = response.json()
        log_message(f"Leads fetched successfully for date: {date}.")
        log_message(f"Response data: {json.dumps(data, indent=4)}")
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
    Main function fetches leads from the AmoCRM for a specific date.
    Handles exceptions and logs errors.
    """
    try:
        # Set the date manually in 'Y-m-d' format
        date = "2025-04-17"
        log_message(f"Fetching leads from {domain} for date {date} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Fetch leads for the specified date
        leads = load_leads(date)
        
    except Exception as e:
        # Log any errors that occur
        log_message(f"Error: {str(e)}")


if __name__ == "__main__":
    main()