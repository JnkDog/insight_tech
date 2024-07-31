import subprocess

class RequestHandler:
    def __init__(self):
        self.requests_available = self.check_requests()

    def check_requests(self):
        try:
            import requests
            return True
        except ImportError:
            return False

    def fetch_using_requests(self, url):
        import requests
        response = requests.get(url)
        return response.text

    def fetch_using_curl(self, url):
        result = subprocess.run(['curl', url], capture_output=True, text=True)
        return result.stdout

    def fetch(self, url):
        if self.requests_available:
            print(f"Using requests library for {url}.")
            return self.fetch_using_requests(url)
        else:
            print(f"requests library not available. Using curl for {url}.")
            return self.fetch_using_curl(url)

    def fetch_multiple(self, urls):
        responses = {}
        for url in urls:
            responses[url] = self.fetch(url)
        return responses

if __name__ == "__main__":
    urls = [
        'http://www.example.com',
        'http://www.example.org',
        'http://www.example.net'
    ]
    handler = RequestHandler()
    responses = handler.fetch_multiple(urls)
    for url, response in responses.items():
        print(f"Response from {url}:")
        print(response)
        print("\n" + "="*80 + "\n")