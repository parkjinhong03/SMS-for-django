from .exceptions import DependencyNotImplementedError


class Base:
    dependency_interfaces = ()

    @classmethod
    def dependency_duck_typing(cls, *dependencies):
        dependencies = dependencies if dependencies else ()

        for dependency, interface in zip(dependencies, cls.dependency_interfaces):
            if not isinstance(dependency, interface):
                raise DependencyNotImplementedError(dependency, interface)
