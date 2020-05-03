import inspect
import typing

from . import types


def Class(cls):
    type_annotations = typing.get_type_hints(cls.__init__)
    dependency_names = inspect.getfullargspec(cls.__init__).args[1:]

    return types.DependencySpec(
        dependency_types=[
            type_annotations[dependency_name] for dependency_name in dependency_names
        ],
        instantiate=cls,
    )


def Function(fn):
    type_annotations = typing.get_type_hints(fn)
    arg_names = inspect.getfullargspec(fn).args

    return types.DependencySpec(
        dependency_types=[type_annotations[arg_name] for arg_name in arg_names],
        instantiate=fn,
    )


def Value(value):
    return types.DependencySpec(dependency_types=[], instantiate=lambda: value)


def to_dependency_spec(factory: typing.Any) -> types.DependencySpec:
    if isinstance(factory, types.DependencySpec):
        return factory

    if inspect.isclass(factory):
        return Class(factory)

    if inspect.isfunction(factory) or inspect.ismethod(factory):
        return Function(factory)

    return Value(factory)
