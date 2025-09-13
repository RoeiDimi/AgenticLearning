import requests
import json

url = "https://x9ct8azu9d.execute-api.us-east-1.amazonaws.com/prod/mcp"

def plain_http_post_example():
    # Example 1: Simple HTTP POST using requests
    headers = {"Content-Type": "application/json"}

    # Call the 'add' tool
    payload = {"method": "add", "params": {"a": 2, "b": 3}}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("HTTP POST response:", response.json())

if __name__ == "__main__":
    plain_http_post_example()
