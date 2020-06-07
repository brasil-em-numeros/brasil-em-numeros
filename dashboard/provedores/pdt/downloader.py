import requests

from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO


def download(url_list, transform = lambda x: x, *args, **kwargs):
    
    """
    Tranform é uma função que manipula o output uma vez que o download foi completado
    Ela é responsável por lidar com qualquer tipo de erro
    O valor padrão de transform é a função identidade, ou seja, não muda o output
    """
    
    processes = []
    with ThreadPoolExecutor(max_workers=36) as executor:
        for url in url_list:
            processes.append(executor.submit(_download_csv, url))

    # responses = []
    for task in as_completed(processes):
        yield transform(task.result(), *args, **kwargs)

    # return responses


def _download_csv(url):
    resp = requests.get(url, stream=True)
    return BytesIO(resp.content)
