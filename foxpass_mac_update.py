import os
import requests
import json
import logging
from icecream import ic
from dotenv import load_dotenv
from mac import MacAddress
from urllib.parse import quote
from utils import setup_logging
import config
import argparse

logger = logging.getLogger(__name__)
env_path = os.path.join(os.path.expanduser("~"), ".env")
load_dotenv()

class Foxpass:
    BASE_URL = 'https://api.foxpass.com/v1/'

    def __init__(self, api_key):

        self.headers = {
            "accept": "application/json",
            'Authorization': f'Token {api_key}'
        }

    def all(self, endpoint: str) -> list:
        """
        Retrieve and compile all paginated data from an API endpoint.

        This method sends a GET request to the specified API endpoint and iteratively
        fetches all paginated data, appending them to a single list until no additional
        pages are available. It assumes the paginated structure includes a
        'results' key for data records and a 'next' key indicating the next page URL.

        :param endpoint: The API endpoint to gather data from
        :type endpoint: str
        :return: A list of all the gathered data records
        :rtype: list
        """
        url = f'{self.BASE_URL}{endpoint}'
        all_data = []

        while url:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                break

            data = response.json()
            if data.get('status') == 'ok':

                all_data.extend(data.get('data', []))  # Assuming 'results' holds the paginated data

                # Check if there is a `next` URL in the response (e.g., in the headers or in the JSON body)
                url = data.get('next')  # Adjust depending on where the `next` page information is located
            else:
                logger.error(f"Request failed with status code {response.status_code}: {data.get('status')}")
        return all_data

    def get(self, endpoint: str, item: str) -> dict:
        """
        Fetches data from a specified endpoint and item while handling errors and logging.

        This method sends a GET request to a constructed URL formed by combining the
        BASE_URL, endpoint, and item. If the response status code is not 200, it logs an
        error message and returns an empty dictionary. If the response status is 'ok',
        it extracts and returns the data part of the JSON response.

        :param endpoint: The specific API endpoint to send the GET request to.
        :type endpoint: str
        :param item: The resource or item to be appended to the endpoint for querying.
        :type item: str
        :return: The extracted 'data' key from the JSON response if successful, or an
                 empty dictionary otherwise.
        :rtype: dict
        """
        url = f'{self.BASE_URL}{endpoint}{item}'

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            logger.debug(f"Request failed with status code {response.status_code}: {response.text}")
            return {}
        else:
            data = response.json()
            if data.get('status') == 'ok':
                return data.get('data')

    def create(self, endpoint: str, data: dict) -> dict:
        """
        Sends a POST request to the specified endpoint with the given data and
        returns the JSON response. If the request fails (non-200 status code),
        logs the error and returns an empty dictionary.

        :param endpoint: The API endpoint to which the POST request will be sent.
        :type endpoint: str
        :param data: The JSON serializable dictionary that contains the payload
            to be sent in the body of the POST request.
        :type data: dict
        :return: The response from the POST request as a dictionary if the
            request is successful, or an empty dictionary if the request fails.
        :rtype: dict
        """
        self.headers['Content-Type'] = 'application/json'
        url = f'{self.BASE_URL}{endpoint}'
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code != 200:
            logger.debug(f"Request failed with status code {response.status_code}: {response.text}")
            return {}
        else:
            return response.json()

    def update(self, endpoint: str, item: str, data: dict) -> dict:
        """
        Updates a specific item at a given endpoint using a PUT request.

        This method constructs the full URL using the provided `endpoint` and `item`,
        then sends a PUT request with the given `data` in JSON format. It uses the
        configured base URL and headers for the request. Logs an error message if the
        request fails with a status code other than 200. Returns the JSON response in
        case of a successful request.

        :param endpoint: The API endpoint to which the update request is sent.
        :type endpoint: str
        :param item: The specific item to be updated in the API.
        :type item: str
        :param data: The payload to be sent in the PUT request, formatted as a dictionary.
        :type data: dict
        :return: The JSON response from the API if the request is successful.
        :rtype: dict
        """
        url = f'{self.BASE_URL}{endpoint}{item}'
        response = requests.put(url, headers=self.headers, json=data)
        if response.status_code != 200:
            logger.debug(f"Request failed with status code {response.status_code}: {response.text}")
        else:
            return response.json()

    def delete(self, endpoint: str, item: str) -> dict:
        """
        Deletes a specific resource identified by the `endpoint` and `item` from a server. The function constructs
        a URL using the base URL, `endpoint`, and `item` provided, and performs a DELETE request to the
        specified resource. If the DELETE request fails (HTTP status code other than 200), an error will
        be logged. On success, the response from the server is returned.

        :param endpoint: The API endpoint specifying the resource's base path.
        :type endpoint: str
        :param item: The identifier of the specific resource to delete.
        :type item: str
        :return: The JSON response from the server if the DELETE request is successful.
        :rtype: dict
        """
        url = f'{self.BASE_URL}{endpoint}{item}/'
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200:
            logger.debug(f"Request failed with status code {response.status_code}: {response.text}")
        else:
            return response.json()

class MacFoxpass(Foxpass):
    """
    Manages MAC address groups and their entries through the Foxpass API.

    This class provides functionalities to handle MAC groups and their respective
    MAC addresses. It offers methods to add, delete, query, and list MAC groups
    and their entries while communicating with the Foxpass API.

    :ivar ENDPOINT: The endpoint for interacting with MAC entries
    :type ENDPOINT: str
    """
    ENDPOINT = 'mac_entries/'

    def __init__(self, api_key):
        super().__init__(api_key)

    def add_mac_group(self, group_name: str) -> dict:
        endpoint = self.ENDPOINT
        return self.create(endpoint, {'name': group_name})

    def delete_mac_group(self, group_name: str) -> None:
        endpoint = self.ENDPOINT
        return self.delete(endpoint, group_name)

    def get_mac_group(self, group_name: str) -> dict:
        endpoint = f'{self.ENDPOINT}'
        return self.get(endpoint, group_name)

    def list_mac_groups(self) -> list:
        endpoint = self.ENDPOINT
        return self.all(endpoint)

    def list_mac_entries(self, group_name: str) -> list:
        """
        List all MAC entries in a specific group.

        :param group_name: The MAC group to list entries from
        :type group_name: str
        :return: A list of all MAC entries in the group
        :rtype: list
        """
        endpoint = f'{self.ENDPOINT}{group_name}/prefixes/'
        return self.all(endpoint)

    def add_mac_entry(self, group_name: str, mac_address: str, ) -> dict:
        """
        Add a MAC address to a specific group.

        :param group_name: The MAC group to add the entry to
        :type group_name: str
        :param mac_address: The MAC address to be added
        :type mac_address: str
        :return: Response from the API
        :rtype: dict
        """
        return self.update(
            f'{self.ENDPOINT}',f'{group_name}/prefixes/',{'prefix': mac_address})

    def delete_mac_entry(self, group_name: str, mac_address: str) -> None:
        """
        Delete a MAC address from a specific group.

        :param group_name: The MAC group to delete the entry from
        :type group_name: str
        :param mac_address: The MAC address to be deleted
        :type mac_address: str
        """
        endpoint = f'{self.ENDPOINT}{group_name}/'
        self.delete(endpoint, mac_address)

    def is_mac_in_group(self, group_name: str, mac_address: str) -> bool:
        """
        Checks if a given MAC address is present in a specified group.

        This function performs a GET request to an external service, using the
        group name and MAC address as path parameters, to determine whether the
        specified MAC address is associated with the group. If the request is
        successful and the response indicates a positive match, it returns True.
        Otherwise, it returns False. If the request fails, it logs an error and
        returns False.

        :param group_name: The name of the group being queried.
        :param mac_address: The MAC address being checked in the group.
        :return: A boolean value indicating whether the MAC address exists in
                 the group.
        """
        url = f'{self.BASE_URL}{self.ENDPOINT}{group_name}/prefixes/{mac_address}/'
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logger.error(f"Request failed with status code {response.status_code}: {response.text}")
            return False
        else:
            data = response.json()
            if data.get('status') == 'ok':
                return True
            else:
                return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=f"Meraki Site Sync")

    # Add the verbose flag
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output (debug level logging)"
    )

    parser.add_argument(
        "--mac-group",
        type=str,
        help="The name of the MAC Address Group."
    )

    parser.add_argument(
        "--mac-address-file",
        type=str,
        help="The file containing the MAC addresses to add."
    )

    args = parser.parse_args()
    if args.verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)

    try:
        foxpass_api_key = os.environ['FOXPASS_API_KEY']
    except KeyError:
        logger.critical(f'Please set the FOXPASS_API_KEY environment variable.')
        raise SystemExit(1)

    macs = MacFoxpass(foxpass_api_key)

    if args.mac_group:
        if not args.mac_address_file:
            logger.critical(f'Please specify the filename containing the MAC addresses to add with --mac-address-file [filename.txt].')
            raise SystemExit(1)

        # Validate that the group exists before trying to add to it.
        mac_group = macs.get_mac_group(args.mac_group)
        if not mac_group:
            logger.critical(f'Group <{args.mac_group}> does not exist. Please create it first.')
            raise SystemExit(1)

        file_path = os.path.join(config.INPUT_DIR, args.mac_address_file)
        with open(file_path, 'r') as file:
            mac_addresses = [line.strip() for line in file if line.strip()]

        for mac_address in mac_addresses:
            try:
                good_mac = MacAddress(mac_address)
            except ValueError as e:
                logger.warning(f'MAC Address {mac_address} provided in {args.mac_address_file} is not valid. Skipping.')
                continue

            # Add the mac address to Foxpass
            add_mac = macs.add_mac_entry(args.mac_group, good_mac.mac_address)
