import typing

from . import types

ResolveDependency = typing.Callable[[types.DependencyType], typing.Any]
