import typing

from . import types


class CargoException(Exception):
    pass


class DependencyNotFound(CargoException):
    pass


class CircularDependency(CargoException):
    cycle: typing.List[types.DependencyType]

    def __init__(self, cycle: typing.List[types.DependencyType]):
        super().__init__(cycle)
        self.cycle = cycle


class NoMiddlewares(CargoException):
    pass
