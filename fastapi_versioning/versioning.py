from collections import defaultdict
from typing import Tuple, Callable, Dict, List

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.datastructures import Headers
from starlette.routing import Match
from starlette.types import Scope


def version(major: int, minor: int):
    def decorator(func: Callable) -> Callable:
        func.__api_version__ = (major, minor)
        return func
    return decorator

def version_to_route(route: APIRoute) -> Tuple[int, APIRoute]:
    version = getattr(route.endpoint, '__api_version__', (1, 0))
    return version, route

def VersionedFastAPI(
    app: FastAPI,
    version_format: str = '{major}.{minor}',
    prefix_format: str = '/v{major}_{minor}',
    **kwargs,
) -> FastAPI:
    parent_app = FastAPI(
        title=app.title,
        **kwargs,
    )
    version_route_mapping: Dict[str, List[APIRoute]] = defaultdict(list)
    for version, route in map(version_to_route, app.routes):
        version_route_mapping[version].append(route)

    unique_routes = {}
    for version in sorted(version_route_mapping.keys()):
        major, minor = version
        prefix = prefix_format.format(major=major, minor=minor)
        semver = version_format.format(major=major, minor=minor)
        versioned_app = FastAPI(
            title=app.title,
            version=semver,
            openapi_prefix=prefix,
        )
        for route in version_route_mapping[version]:
            for method in route.methods:
                unique_routes[route.path + '|' + method] = route
        for route in unique_routes.values():
            versioned_app.router.routes.append(route)
        parent_app.mount(prefix, versioned_app)
        @parent_app.get(
            f'{prefix}/openapi.json',
            name=semver,
            tags=['Versions']
        )
        def noop(): ...

    return parent_app
