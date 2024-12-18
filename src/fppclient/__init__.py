"""Asynchronous Python client for FPP."""

from .exceptions import (
    FPPConnectionClosedError,
    FPPConnectionError,
    FPPConnectionTimeoutError,
    FPPError,
    FPPUnsupportedVersionError,
    FPPUpgradeError,
)
from .fpp import FPP
from .models import Device, SystemStatus

__all__ = [
    "FPP",
    "Device",
    "FPPConnectionClosedError",
    "FPPConnectionError",
    "FPPConnectionTimeoutError",
    "FPPError",
    "FPPUnsupportedVersionError",
    "FPPUpgradeError",
    "SystemStatus",
]
