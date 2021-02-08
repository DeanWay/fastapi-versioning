from collections import defaultdict
from typing import Tuple, Callable, Dict, List

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.datastructures import Headers
from starlette.routing import Match
from starlette.types import Scope


def version(major: int, minor: int = 0):
    def decorator(func: Callable) -> Callable:
        func._api_version = (major, minor)
        return func
    return decorator


def version_to_route(
    route: APIRoute,
    default_version: Tuple[int, int],
) -> Tuple[Tuple[int, int], APIRoute]:
    version = getattr(route.endpoint, '_api_version', default_version)
    return version, route


def VersionedFastAPI(
    app: FastAPI,
    version_format: str = '{major}.{minor}',
    prefix_format: str = '/v{major}_{minor}',
    default_version: Tuple[int, int] = (1, 0),
    **kwargs,
) -> FastAPI:
    parent_app = FastAPI(
        title=app.title,
        **kwargs,
    )
    version_route_mapping: Dict[str, List[APIRoute]] = defaultdict(list)
    version_routes = [version_to_route(route, default_version) for route in app.routes]

    for version, route in version_routes:
        version_route_mapping[version].append(route)

    unique_routes = {}
    for version in sorted(version_route_mapping.keys()):
        major, minor = version
        prefix = prefix_format.format(major=major, minor=minor)
        semver = version_format.format(major=major, minor=minor)
        versioned_app = FastAPI(
            title=app.title,
            description=app.description,
            version=semver,
            root_path=prefix,
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
