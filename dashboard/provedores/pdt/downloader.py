import requests

from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO


def download(url_list):
    processes = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in url_list:
            processes.append(executor.submit(_download_csv, url))

    responses = []
    for task in as_completed(processes):
        responses.append(task.result())

    return responses


def _download_csv(url):
    resp = requests.get(url, stream=True)
    return BytesIO(resp.content)
