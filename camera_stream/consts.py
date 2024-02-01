import enum


class ZoneTopicType(enum.StrEnum):
    ACTIVATION = "zone/activation"
    CORRECTION = "zone/correction"
    CONFIRMATION = "zone/confirmation"
