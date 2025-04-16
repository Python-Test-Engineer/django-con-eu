**API Request Using Requests Library**
=====================================

Below is an example implementation of requesting an API using the Requests library in Python.

### Installation

Before using the Requests library, ensure it's installed. You can install it via pip:

```bash
pip install requests
```

### Implementation

```python
import requests
import json

def make_api_request(url, method='GET', headers=None, params=None, data=None):
    """
    Makes an API request using the Requests library.

    Args:
    - url (str): The URL of the API endpoint.
    - method (str): The HTTP method (default is 'GET').
    - headers (dict): A dictionary of headers (default is None).
    - params (dict): A dictionary of query parameters (default is None).
    - data (dict): A dictionary of data to be sent in the request body (default is None).

    Returns:
    - response (requests.Response): The API response.
    """

    # Map the method to the corresponding Requests function
    methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete
    }

    # Check if the method is valid
    if method.upper() not in methods:
        raise ValueError(f"Invalid method '{method}'. Supported methods are {list(methods.keys())}")

    # Make the API request
    try:
        response = methods[method.upper()](url, headers=headers, params=params, json=data)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def main():
    # Example usage
    url = "https://jsonplaceholder.typicode.com/posts"
    response = make_api_request(url)

    if response:
        print(json.dumps(response.json(), indent=4))


if __name__ == "__main__":
    main()
```

### Explanation

*   This code defines a `make_api_request` function that takes in the API URL, HTTP method, headers, query parameters, and request body data.
*   It uses the Requests library to make the API request based on the provided method and parameters.
*   The `main` function demonstrates how to use `make_api_request` to fetch data from a sample API endpoint.

### Advice

*   Always handle potential exceptions when making API requests.
*   Use the `response.raise_for_status()` method to raise an exception for 4xx or 5xx status codes.
*   Consider logging or printing error messages for debugging purposes.