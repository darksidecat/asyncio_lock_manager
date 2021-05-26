import inspect
from typing import Any, Dict, Optional, List


def _get_spec(func: callable):
    while hasattr(func, '__wrapped__'):  # Try to resolve decorated callbacks
        func = func.__wrapped__
    return inspect.getfullargspec(func)


def _check_spec(spec: inspect.FullArgSpec, kwargs: dict):
    if spec.varkw:
        return kwargs

    return {k: v for k, v in kwargs.items() if k in set(spec.args + spec.kwonlyargs)}


def inspect_params(obj: Any, skip: Optional[List[str]] = None, **kwargs: Any) -> Dict[str, Any]:
    while hasattr(obj, '__wrapped__'):  # Try to resolve decorated callbacks
        obj = obj.__wrapped__

    if skip is None:
        skip = []
    kwargs = {k: kwargs[k] for k in kwargs if k not in skip}
    spec = _get_spec(obj)

    return _check_spec(spec, kwargs)
