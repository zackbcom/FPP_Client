"""Asynchronous Python client for FPP."""

from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from typing import Any, Self

import aiohttp
import backoff
import orjson
from yarl import URL

from .exceptions import (
    FPPConnectionError,
    FPPConnectionTimeoutError,
    FPPEmptyResponseError,
    FPPError,
)
from .models import Device


@dataclass
class FPP:
    """Main class for handling connections with FPP."""

    host: str
    request_timeout: float = 8.0
    session: aiohttp.client.ClientSession | None = None

    _client: aiohttp.ClientWebSocketResponse | None = None
    _close_session: bool = False
    _device: Device | None = None

    @backoff.on_exception(backoff.expo, FPPConnectionError, max_tries=3, logger=None)
    async def request(
        self,
        uri: str = "",
        method: str = "GET",
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to a FPP device.

        A generic method for sending/handling HTTP requests done gainst
        the FPP device.

        Args:
        ----
            uri: Request URI, for example `/api/system/status`.
            method: HTTP method to use for the request.E.g., "GET" or "POST".
            data: Dictionary of data to send to the FPP device.

        Returns:
        -------
            A Python dictionary (JSON decoded) with the response from the
            FPP device.

        Raises:
        ------
            FPPConnectionError: An error occurred while communication with
                the FPP device.
            FPPConnectionTimeoutError: A timeout occurred while communicating
                with the FPP device.
            FPPError: Received an unexpected response from the FPP device.

        """
        url = URL.build(scheme="http", host=self.host, port=80, path=uri)

        headers = {
            "Accept": "application/json, text/plain, */*",
        }

        if self.session is None:
            self.session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    json=data,
                    headers=headers,
                )

            content_type = response.headers.get("Content-Type", "")
            if response.status // 100 in [4, 5]:
                contents = await response.read()
                response.close()

                if content_type == "application/json":
                    raise FPPError(
                        response.status,
                        orjson.loads(contents),
                    )
                raise FPPError(
                    response.status,
                    {"message": contents.decode("utf8")},
                )

            response_data = await response.text()
            if "application/json" in content_type:
                response_data = orjson.loads(response_data)

        except asyncio.TimeoutError as exception:
            msg = f"Timeout occurred while connecting to FPP device at {self.host}"
            raise FPPConnectionTimeoutError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error occurred while communicating with FPP device at {self.host}"
            raise FPPConnectionError(msg) from exception

        return response_data

    async def update(self) -> Device:
        """Get all information about the device in a single call.

        This method updates all FPP information available with a single API
        call.

        Returns
        -------
            FPP Device data.

        Raises
        ------
            FPPEmptyResponseError: The FPP device returned an empty response.

        """
        data = {}
        if not (system_status := await self.request("/api/system/status")):
            msg = (
                f"FPP device at {self.host} returned an empty API"
                " response on system_status update",
            )
            raise FPPEmptyResponseError(msg)
        data["system_status"] = system_status

        if not (playlists := await self.request("/api/playlists")):
            msg = (
                f"FPP device at {self.host} returned an empty API"
                " response on playlist update",
            )
            raise FPPEmptyResponseError(msg)
        data["playlists"] = playlists

        if not (sequences := await self.request("/api/sequence")):
            msg = (
                f"FPP device at {self.host} returned an empty API"
                " response on sequences update",
            )
            raise FPPEmptyResponseError(msg)
        data["sequences"] = sequences

        if not self._device:
            self._device = Device.from_dict(data)
        else:
            self._device.update_from_dict(data)

        return self._device

    async def close(self) -> None:
        """Close session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The FPP object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
