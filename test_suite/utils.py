import requests


def test_status_code(url):
    res = requests.get(f"http://{url}")
    if res.status_code == 200:
        print("Test 1 Success")

test_status_code("www.google.com")