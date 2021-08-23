from collections import defaultdict
from typing import Any, Callable, Dict, List, Tuple, TypeVar, cast

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute

CallableT = TypeVar("CallableT", bound=Callable[..., Any])


def version(major: int, minor: int = 0) -> Callable[[CallableT], CallableT]:
    def decorator(func: CallableT) -> CallableT:
        func._api_version = (major, minor)  # type: ignore
        return func

    return decorator


def version_to_route(
    route: BaseRoute,
    default_version: Tuple[int, int],
) -> Tuple[Tuple[int, int], APIRoute]:
    api_route = cast(APIRoute, route)
    version = getattr(api_route.endpoint, "_api_version", default_version)
    return version, api_route


def VersionedFastAPI(
    app: FastAPI,
    version_format: str = "{major}.{minor}",
    prefix_format: str = "/v{major}_{minor}",
    default_version: Tuple[int, int] = (1, 0),
    enable_latest: bool = False,
    **kwargs: Any,
) -> FastAPI:
    parent_app = FastAPI(
        title=app.title,
        **kwargs,
    )
    version_route_mapping: Dict[Tuple[int, int], List[APIRoute]] = defaultdict(
        list
    )
    version_routes = [
        version_to_route(route, default_version) for route in app.routes
    ]

    for version, route in version_routes:
        version_route_mapping[version].append(route)

    unique_routes = {}
    versions = sorted(version_route_mapping.keys())
    for version in versions:
        major, minor = version
        prefix = prefix_format.format(major=major, minor=minor)
        semver = version_format.format(major=major, minor=minor)
        versioned_app = FastAPI(
            title=app.title,
            description=app.description,
            version=semver,
        )
        for route in version_route_mapping[version]:
            for method in route.methods:
                unique_routes[route.path + "|" + method] = route
        for route in unique_routes.values():
            versioned_app.router.routes.append(route)
        parent_app.mount(prefix, versioned_app)

        @parent_app.get(
            f"{prefix}/openapi.json", name=semver, tags=["Versions"]
        )
        @parent_app.get(f"{prefix}/docs", name=semver, tags=["Documentations"])
        def noop() -> None:
            ...

    if enable_latest:
        prefix = "/latest"
        major, minor = version
        semver = version_format.format(major=major, minor=minor)
        versioned_app = FastAPI(
            title=app.title,
            description=app.description,
            version=semver,
        )
        for route in unique_routes.values():
            versioned_app.router.routes.append(route)
        parent_app.mount(prefix, versioned_app)

    return parent_app
