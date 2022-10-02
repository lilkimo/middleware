#from compare import compare

from typing import Any, Callable, Iterable
from dataclasses import dataclass
from grequests import get, post, put, delete, send as gsend, AsyncRequest as Request
from gevent import joinall
from multiprocessing import Process

methods: dict[str, Callable] = {
    'GET': get,
    'POST': post,
    'PUT': put,
    'DELETE': delete,
}

@dataclass
class RequestArgs:
    method: str
    path: str
    headers: Any
    body: Any
    params: Any

def requests(urls: Iterable[str], rArgs: RequestArgs):
    rs = [_request(rArgs, url) for url in urls]
    gsend(rs[0], None, stream=False).join()
    Process(target=_process, args=(rs[0].response, rs[1:])).start()
    return rs[0].response

def _request(args: RequestArgs, url: str) -> Request:
    return methods[args.method](
        f'{url}/{args.path}',
        headers=args.headers,
        data=args.body,
        params=args.params
    )

def _process(reference, rs: list[Request]):
    joinall([gsend(r, None, stream=False) for r in rs])
    ref = reference.json()
    for i in range(len(rs)):
        res = None
        if rs[i].response is not None:
            res = rs[i].response.json()
        print(rs[i].url, res)
        #print(compare(ref, res))