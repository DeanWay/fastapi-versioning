from typing import Type

from fastapi.routing import APIRoute


def versioned_api_route(
    major: int = 1,
    minor: int = 0,
    route_class: Type[APIRoute] = APIRoute
) -> Type[APIRoute]:
    class VersionedAPIRoute(route_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.endpoint._api_version = (major, minor)
    return VersionedAPIRoute
