from __future__ import annotations

import abc
import functools
import typing

from . import _types, exceptions, types


class Handler(types.Middleware):
    def __init__(self, resolve_dependency: _types.ResolveDependency):
        self._dependency_specs: typing.Dict[
            types.DependencyType, types.DependencySpec
        ] = {}
        self._resolve_dependency = resolve_dependency

    def bind(
        self, key: types.DependencyType, dependency_spec: types.DependencySpec
    ) -> None:
        self._dependency_specs[key] = dependency_spec

    def execute(
        self,
        dependency_type: types.DependencyType,
        next_middleware: types.NextMiddleware,
    ) -> typing.Any:
        dependency_spec = self._get_dependency_spec(dependency_type)
        dependencies = self._resolve_dependencies(dependency_spec.dependency_types)
        return dependency_spec.instantiate(*dependencies)

    def _resolve_dependencies(
        self, dependency_types: typing.Sequence[types.DependencyType]
    ):
        return [
            self._resolve_dependency(dependency_type)
            for dependency_type in dependency_types
        ]

    def _get_dependency_spec(self, key: types.DependencyType):
        try:
            return self._dependency_specs[key]
        except KeyError:
            raise exceptions.DependencyNotFound(key)


class Container(types.Container):
    def __init__(
        self,
        middleware_factories: typing.Sequence[types.MiddlewareFactory],
        to_dependency_spec: typing.Callable[[typing.Any], types.DependencySpec],
    ):
        self._to_dependency_spec = to_dependency_spec
        middlewares = tuple(
            middleware_factory() for middleware_factory in middleware_factories
        )
        self._handler = Handler(self.__getitem__)
        self._pipeline = Pipeline(middlewares, self._handler)

    def __setitem__(
        self, dependency_type: types.DependencyType, factory: typing.Any
    ) -> None:
        dependency_spec = self._to_dependency_spec(factory)
        self._handler.bind(dependency_type, dependency_spec)

    def __getitem__(
        self, dependency_type: types.DependencyType
    ) -> types.DependencyValue:
        return self._pipeline.execute(dependency_type)


class Pipeline:
    def __init__(
        self, middlewares: typing.Sequence[types.Middleware], handler: Handler
    ):
        self._stages = functools.reduce(
            MiddlewareStage.create, reversed(middlewares), TerminalStage.create(handler)
        )

    def execute(self, key: types.DependencyType) -> types.DependencyValue:
        return self._stages.execute(key)


class Stage(abc.ABC):
    @abc.abstractmethod
    def execute(self, key: types.DependencyType):
        NotImplementedError()


class MiddlewareStage(Stage):
    def __init__(self, next_stage: Stage, middleware: types.Middleware):
        self._middleware = middleware
        self._next_stage = next_stage

    def execute(self, key: types.DependencyType) -> types.DependencyValue:
        return self._middleware.execute(key, lambda: self._next_stage.execute(key))

    @staticmethod
    def create(next_stage: Stage, middleware: types.Middleware) -> Stage:
        return MiddlewareStage(next_stage, middleware)


class TerminalStage(Stage):
    def __init__(self, middleware: types.Middleware):
        self._middleware = middleware

    def execute(self, key: types.DependencyType) -> types.DependencyValue:
        return self._middleware.execute(key, self._should_never_be_called)

    @staticmethod
    def _should_never_be_called():
        raise Exception("It should never be called")

    @staticmethod
    def create(middleware: types.Middleware) -> Stage:
        return TerminalStage(middleware)
