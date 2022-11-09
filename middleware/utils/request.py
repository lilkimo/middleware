from concurrent.futures import Future
from typing import Any, Callable, Iterable
from dataclasses import dataclass
from requests_futures.sessions import FuturesSession

from .compare import compare
from ..models import Request, Comparision

_session = FuturesSession()
methods: dict[str, Callable] = {
    'GET':    _session.get,
    'POST':   _session.post,
    'PUT':    _session.put,
    'DELETE': _session.delete,
}

@dataclass
class RequestArgs:
    method:  str
    path:    str
    headers: Any
    body:    Any
    params:  Any

@dataclass
class Hook:
    enabled: bool = True
    arg:     Any  = None

    def __bool__(self):
        return self.enabled

def requests(urls: Iterable[str], rArgs: RequestArgs):
    urlsIter = iter(urls)
    primaryRequest = _request(rArgs, next(urlsIter), Hook(False))
    for url in urlsIter:
        _request(rArgs, url, Hook(arg=primaryRequest))
    return primaryRequest.result()

def _request(args: RequestArgs, url: str, hook: Hook) -> Future:
    return methods[args.method](
        f'{url}/{args.path}',
        headers=args.headers,
        data=args.body,
        params=args.params,
        hooks={'response': compareHook(hook.arg)} if hook else None
    )

def compareHook(reference):
    # pylint: disable=unused-argument
    def hook(res, *args, **kwargs):
        print(id(reference))
        ref = reference.result()
        #statusCode = ref.status_code == res.status_code
        equals = compare(ref.json(), res.json())
    return hook
