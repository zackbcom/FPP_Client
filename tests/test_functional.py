"""Tests for `fpp.FPP`."""

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from fpp import FPP
from fpp.exceptions import FPPError


@pytest.mark.asyncio
async def test_http_system_status(aresponses: ResponsesMockServer) -> None:
    """Test HTTP 500 response handling."""
    aresponses.add(
        "example.com",
        "/",
        "GET",
        aresponses.Response(
            body=b'{"status":"nok"}',
            status=500,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        fpp = FPP("example.com", session=session)
        with pytest.raises(FPPError):
            assert await fpp.request("/")
