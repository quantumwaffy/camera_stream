import enum

from core import mixins as core_mixins


class ZoneTopicType(enum.StrEnum):
    ACTIVATION = "zone/activation"
    CORRECTION = "zone/correction"
    CONFIRMATION = "zone/confirmation"


class StateZoneType(core_mixins.EnumExtraMethodsMixin):
    ON = 1
    OFF = 0
