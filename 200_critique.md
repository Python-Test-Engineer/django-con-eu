**Requesting an API with the Requests Library**
=====================================================

Below is a Python implementation using the Requests library to request an API. This example will cover the basic usage of the library for GET, POST, PUT, and DELETE requests.

```python
import requests
import json

class APIRequest:
    def __init__(self, base_url):
        """
        Initialize the APIRequest class.

        Args:
            base_url (str): The base URL of the API.
        """
        self.base_url = base_url

    def get(self, endpoint, params=None, headers=None):
        """
        Send a GET request to the API.

        Args:
            endpoint (str): The endpoint of the API.
            params (dict, optional): The query parameters. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.

        Returns:
            Response: The response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, params=params, headers=headers)

    def post(self, endpoint, data=None, json=None, headers=None):
        """
        Send a POST request to the API.

        Args:
            endpoint (str): The endpoint of the API.
            data (dict, optional): The request data. Defaults to None.
            json (dict, optional): The JSON data. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.

        Returns:
            Response: The response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        return requests.post(url, data=data, json=json, headers=headers)

    def put(self, endpoint, data=None, json=None, headers=None):
        """
        Send a PUT request to the API.

        Args:
            endpoint (str): The endpoint of the API.
            data (dict, optional): The request data. Defaults to None.
            json (dict, optional): The JSON data. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.

        Returns:
            Response: The response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        return requests.put(url, data=data, json=json, headers=headers)

    def delete(self, endpoint, params=None, headers=None):
        """
        Send a DELETE request to the API.

        Args:
            endpoint (str): The endpoint of the API.
            params (dict, optional): The query parameters. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.

        Returns:
            Response: The response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        return requests.delete(url, params=params, headers=headers)


# Example usage
if __name__ == "__main__":
    api = APIRequest("https://jsonplaceholder.typicode.com")

    # Send a GET request
    response = api.get("/posts")
    print("GET Response:", response.status_code)
    print("GET Data:", response.json())

    # Send a POST request
    data = {
        "title": "Test Post",
        "body": "This is a test post",
        "userId": 1
    }
    response = api.post("/posts", json=data)
    print("POST Response:", response.status_code)
    print("POST Data:", response.json())

    # Send a PUT request
    data = {
        "id": 1,
        "title": "Updated Post",
        "body": "This is an updated post",
        "userId": 1
    }
    response = api.put("/posts/1", json=data)
    print("PUT Response:", response.status_code)
    print("PUT Data:", response.json())

    # Send a DELETE request
    response = api.delete("/posts/1")
    print("DELETE Response:", response.status_code)
```

This implementation provides a basic structure for sending requests to an API using the Requests library. The `APIRequest` class encapsulates the base URL and provides methods for sending GET, POST, PUT, and DELETE requests. The example usage demonstrates how to use the class to send requests to the JSONPlaceholder API.