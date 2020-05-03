import abc
import typing

DependencyValue = typing.TypeVar("DependencyValue")
DependencyType = typing.Type[DependencyValue]


class Container(abc.ABC):
    @abc.abstractmethod
    def __setitem__(self, dependency_type: DependencyType, factory: typing.Any) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def __getitem__(self, dependency_type: DependencyType) -> DependencyValue:
        raise NotImplementedError()


class DependencySpec(typing.NamedTuple):
    dependency_types: typing.Sequence[DependencyType]
    instantiate: typing.Callable[..., typing.Any]


NextMiddleware = typing.Callable[[], typing.Any]


class Middleware(abc.ABC):
    @abc.abstractmethod
    def execute(
        self, dependency_type: DependencyType, next_middleware: NextMiddleware,
    ):
        raise NotImplementedError()


MiddlewareFactory = typing.Union[
    typing.Type[Middleware], typing.Callable[[], Middleware]
]
