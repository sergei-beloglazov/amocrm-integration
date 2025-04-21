import requests
import json
import os
from datetime import datetime, timedelta
from settings import token, domain, logsPath
import base64


def log_message(message):
    """Logs a message to a file with a timestamp."""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_filename = os.path.join(
        logsPath, "info_"+datetime.now().strftime("%Y-%m-%d") + ".txt")
    with open(log_filename, "a") as log_file:
        log_file.write(f"{timestamp} {message}\n")


def get_lead_info(lead_id):
    """
    Fetches notes for a specific lead from the AmoCRM.
    """
    # Updated: Changed the endpoint to fetch notes for a specific lead
    function = f"/api/v4/leads/{lead_id}/notes"  # Endpoint for lead notes
    url = f"https://{domain}{function}"
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {token}"  # Authorization using Bearer token
    }
    
    # Send GET request to the API
    response = requests.get(url, headers=headers)
    
    # Handle HTTP response codes
    if response.status_code == 200:
        # Success: Parse and return the response data
        data = response.json()
        log_message("Notes fetched successfully.")
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


def decode_lead_info(lead_info):
    """
    Decodes the 'link' parameter from the notes in the lead_info JSON.
    Logs the audio recording URL and the decoded parts.

    Parameters:
        lead_info (dict): JSON object containing lead information, including notes.
    """
    notes = lead_info.get('_embedded', {}).get('notes', [])
    
    for note in notes:
        params = note.get('params', {})

        
        link = params.get('link')
        if link and '.onpbx.ru' in link:
            log_message(f"*** Found onlinePBX audio recording: {link}")
            
            # Extract the base64 parts from the link
            try:
                base64_parts = link.split("download_amocrm/")[1].split("/rec.mp3")[0].split("_")
                
                if len(base64_parts) == 2:
                    decoded_info =  base64.b64decode(base64_parts[0]).decode('utf-8')
                    log_message(f"Decoded info: "+decoded_info)
                else:
                    log_message("Error: Unexpected format in the link.")
            except Exception as e:
                log_message(f"Error decoding link: {str(e)}")


def main():
    """
    Main function fetch leads from the AmoCRM 
    Handles exceptions and logs errors.
    """
    try:
        log_message(
            f"Fetching leads from {domain} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        lead_id=23745341
        # Fetch leads
        lead_info = get_lead_info(lead_id)
        decode_lead_info(lead_info)
    except Exception as e:
        # Log any errors that occur
        log_message(f"Error: {str(e)}")


if __name__ == "__main__":
    main()