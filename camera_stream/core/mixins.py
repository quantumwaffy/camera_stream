import enum


class EnumExtraMethodsMixin(enum.Enum):
    @classmethod
    @property
    def values(cls) -> tuple[str, ...]:
        return tuple(item.value for item in cls.__members__.values())

    @classmethod
    @property
    def names(cls) -> tuple[str, ...]:
        return tuple(cls.__members__)

    @classmethod
    @property
    def name_value(cls) -> dict[str, str | int]:
        return {item.name: item.value for item in cls.__members__.values()}
