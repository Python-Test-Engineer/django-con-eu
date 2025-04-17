**API Request with Requests Library**
======================================

Below is an example implementation of requesting an API using the Requests library in Python.

```python
import requests
import json

class APIRequest:
    def __init__(self, base_url: str, headers: dict = None, params: dict = None):
        """
        Initialize the API request.

        Args:
        - base_url (str): The base URL of the API.
        - headers (dict): The headers to be included in the request. Defaults to None.
        - params (dict): The parameters to be included in the request. Defaults to None.
        """
        self.base_url = base_url
        self.headers = headers if headers else {}
        self.params = params if params else {}

    def get(self, endpoint: str):
        """
        Send a GET request to the API.

        Args:
        - endpoint (str): The endpoint of the API.

        Returns:
        - response (requests.Response): The response from the API.
        """
        try:
            response = requests.get(
                url=f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=self.params
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            return response
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Something went wrong: {err}")

    def post(self, endpoint: str, data: dict):
        """
        Send a POST request to the API.

        Args:
        - endpoint (str): The endpoint of the API.
        - data (dict): The data to be sent in the request body.

        Returns:
        - response (requests.Response): The response from the API.
        """
        try:
            response = requests.post(
                url=f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=self.params,
                data=json.dumps(data)
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            return response
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Something went wrong: {err}")


# Example usage
if __name__ == "__main__":
    base_url = "https://jsonplaceholder.typicode.com"
    headers = {
        "Content-Type": "application/json"
    }

    api_request = APIRequest(base_url, headers)
    endpoint = "/posts"

    # Send a GET request
    response = api_request.get(endpoint)
    print(response.json())

    # Send a POST request
    data = {
        "title": "Example Post",
        "body": "This is an example post",
        "userId": 1
    }
    response = api_request.post(endpoint, data)
    print(response.json())
```

### Explanation:

*   We define a class `APIRequest` to handle API requests.
*   The `__init__` method initializes the API request with a base URL, headers, and parameters.
*   The `get` method sends a GET request to the API with the specified endpoint and returns the response.
*   The `post` method sends a POST request to the API with the specified endpoint and data, and returns the response.
*   We use the `requests` library to send the HTTP requests and handle exceptions.
*   In the example usage, we demonstrate how to send a GET request and a POST request to the JSONPlaceholder API.