import dataclasses


@dataclasses.dataclass(frozen=True)
class Style:
    r: int
    g: int
    b: int
    thickness: int

    @property
    def bgr(self) -> tuple[int, ...]:
        return (
            self.b,
            self.g,
            self.r,
        )


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    @property
    def coords(self) -> tuple[int, int]:
        return self.x, self.y


@dataclasses.dataclass(frozen=True)
class Rectangle:
    start: Point
    end: Point
    style: Style
