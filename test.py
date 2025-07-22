import requests
import json

def main():
    """
    Connects to a Webdis server to set and get a key.
    """
    # --- Configuration ---
    # Replace with the actual host and port where your Webdis is running.
    webdis_host = "gork"
    webdis_port = 7379
    base_url = f"http://{webdis_host}:{webdis_port}"

    # The key we will use for our demonstration.
    my_key = "my_special_key"

    print(f"Using Webdis at: {base_url}")

    # --- 1. Set a Key with an Empty Value ---
    # Webdis maps HTTP requests to Redis commands. To set a key, we use the SET command.
    # The URL format is /<COMMAND>/<key>/<value>
    # To set a key with an empty value, we provide an empty string for the value.
    set_url = f"{base_url}/SET/{my_key}/" # The trailing slash represents an empty value
    print(f"\nAttempting to set key '{my_key}' with an empty value...")
    print(f"Request URL: {set_url}")

    try:
        response = requests.get(set_url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Webdis returns a JSON response.
        response_data = response.json()

        # A successful SET command returns: {"SET":[true,"OK"]}
        if response_data.get("SET") and response_data["SET"][0]:
            print(f"Successfully set key '{my_key}'.")
            print(f"Response from Webdis: {json.dumps(response_data)}")
        else:
            print(f"Failed to set key '{my_key}'.")
            print(f"Response: {json.dumps(response_data)}")
            return

    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred while trying to connect to Webdis: {e}")
        print("Please ensure that Webdis is running and accessible at the specified host and port.")
        return

    # --- 2. Get the Key Back ---
    # To retrieve the key, we use the GET command.
    # The URL format is /<COMMAND>/<key>
    get_url = f"{base_url}/GET/{my_key}"
    print(f"\nAttempting to get key '{my_key}'...")
    print(f"Request URL: {get_url}")

    try:
        response = requests.get(get_url)
        response.raise_for_status()

        response_data = response.json()

        # A successful GET command returns the value.
        retrieved_value = response_data.get("GET")

        if retrieved_value is not None:
            print(f"Successfully retrieved key '{my_key}'.")
            # The value will be an empty string in this case.
            print(f"Value: '{retrieved_value}'")
        else:
            print(f"Could not retrieve key '{my_key}'. It may not exist.")
            print(f"Response: {json.dumps(response_data)}")

    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

