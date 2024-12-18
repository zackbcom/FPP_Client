"""Exceptions for FPP."""


class FPPError(Exception):
    """Generic FPP exception."""


class FPPEmptyResponseError(Exception):
    """FPP empty API response exception."""


class FPPConnectionError(FPPError):
    """FPP connection exception."""


class FPPConnectionTimeoutError(FPPConnectionError):
    """FPP connection Timeout exception."""


class FPPConnectionClosedError(FPPConnectionError):
    """FPP WebSocket connection has been closed."""


class FPPUnsupportedVersionError(FPPError):
    """FPP version is unsupported."""


class FPPUpgradeError(FPPError):
    """FPP upgrade exception."""
