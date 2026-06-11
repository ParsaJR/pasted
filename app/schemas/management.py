from pydantic.dataclasses import dataclass


@dataclass
class ExpiryDuration():
    name: str
    code: str

@dataclass
class APICapabilities():
    """Used to inform the clients about the available options."""
    expiry_durations: list[ExpiryDuration]
