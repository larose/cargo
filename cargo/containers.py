import typing

from . import _container, dependency_specs, middlewares, types


def Standard():
    middleware_factories = [
        middlewares.CircularDependencyCircuitBreaker,
        middlewares.Singleton,
    ]

    return _container.Container(
        middleware_factories, dependency_specs.to_dependency_spec
    )


def create(
    middleware_factories: typing.Sequence[types.MiddlewareFactory],
    to_dependency_spec: typing.Callable[
        [typing.Any], types.DependencySpec
    ] = dependency_specs.to_dependency_spec,
) -> types.Container:
    return _container.Container(middleware_factories, to_dependency_spec)
