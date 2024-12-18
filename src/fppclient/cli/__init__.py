"""Asynchronous Python client for FPP."""

import asyncio
import sys
from typing import Annotated

import typer
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from zeroconf import ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf

from fppclient import FPP
from fppclient.exceptions import FPPConnectionError, FPPUnsupportedVersionError

from .async_typer import AsyncTyper

cli = AsyncTyper(help="FPP CLI", no_args_is_help=True, add_completion=False)
console = Console()


@cli.error_handler(FPPConnectionError)
def connection_error_handler(_: FPPConnectionError) -> None:
    """Handle connection errors."""
    message = """
    Could not connect to the specified FPP device. Please make sure that
    the device is powered on, connected to the network and that you have
    specified the correct IP address or hostname.

    If you are not sure what the IP address or hostname of your FPP device
    is, you can use the scan command to find it:

    fpp scan
    """
    panel = Panel(
        message,
        expand=False,
        title="Connection error",
        border_style="red bold",
    )
    console.print(panel)
    sys.exit(1)


@cli.error_handler(FPPUnsupportedVersionError)
def unsupported_version_error_handler(
    _: FPPUnsupportedVersionError,
) -> None:
    """Handle unsupported version errors."""
    message = """
    The specified FPP device is running an unsupported version.

    Currently only 0.14.0 and higher is supported
    """
    panel = Panel(
        message,
        expand=False,
        title="Unsupported version",
        border_style="red bold",
    )
    console.print(panel)
    sys.exit(1)


@cli.command("info")
async def command_info(  # noqa: PLR0915
    host: Annotated[
        str,
        typer.Option(
            help="FPP device IP address or hostname",
            prompt="Host address",
            show_default=False,
        ),
    ],
) -> None:
    """Show the information about the FPP device."""
    with console.status("[cyan]Fetching FPP device information...", spinner="toggle12"):
        async with FPP(host) as dev:
            device = await dev.update()

    info_table = Table(title="\nFPP device information", show_header=False)
    info_table.add_column("Property", style="cyan bold")
    info_table.add_column("Value", style="green")

    info_table.add_row("FPP Status", device.system_status.fppd)
    info_table.add_row("mode_name", device.system_status.mode_name)
    info_table.add_row("volume", str(device.system_status.volume))
    info_table.add_row("current_sequence", device.system_status.current_sequence)
    info_table.add_row("current_song", device.system_status.current_song)
    info_table.add_row("seconds_played", str(device.system_status.seconds_played))
    info_table.add_row("seconds_elapsed", str(device.system_status.seconds_elapsed))
    info_table.add_row("seconds_remaining", str(device.system_status.seconds_remaining))
    info_table.add_row("repeat_mode", str(device.system_status.repeat_mode))

    info_table.add_section()
    if device.system_status.current_playlist:
        info_table.add_row(
            "current_playlist: count", str(device.system_status.current_playlist.count)
        )
        info_table.add_row(
            "current_playlist: description",
            device.system_status.current_playlist.description,
        )
        info_table.add_row(
            "current_playlist: index", str(device.system_status.current_playlist.index)
        )
        info_table.add_row(
            "current_playlist: playlist", device.system_status.current_playlist.playlist
        )
        info_table.add_row(
            "current_playlist: type", device.system_status.current_playlist.type
        )

    info_table.add_section()
    if device.system_status.MQTT:
        info_table.add_row(
            "MQTT: configured", str(device.system_status.MQTT.configured)
        )
        info_table.add_row("MQTT: connected", str(device.system_status.MQTT.connected))

    info_table.add_section()
    if device.system_status.advancedView:
        info_table.add_row(
            "AdvView: HostName", device.system_status.advancedView.HostName
        )
        info_table.add_row(
            "AdvView: HostDescription",
            device.system_status.advancedView.HostDescription,
        )
        info_table.add_row(
            "AdvView: Platform", device.system_status.advancedView.Platform
        )
        info_table.add_row(
            "AdvView: Variant", device.system_status.advancedView.Variant
        )
        info_table.add_row("AdvView: Mode", device.system_status.advancedView.Mode)
        info_table.add_row(
            "AdvView: Version", device.system_status.advancedView.Version
        )
        info_table.add_row("AdvView: Branch", device.system_status.advancedView.Branch)
        info_table.add_row(
            "AdvView: OSVersion", device.system_status.advancedView.OSVersion
        )
        info_table.add_row(
            "AdvView: OSRelease", device.system_status.advancedView.OSRelease
        )
        info_table.add_row(
            "AdvView: channelRanges", device.system_status.advancedView.channelRanges
        )
        info_table.add_row(
            "AdvView: majorVersion", str(device.system_status.advancedView.majorVersion)
        )
        info_table.add_row(
            "AdvView: minorVersion", str(device.system_status.advancedView.minorVersion)
        )
        info_table.add_row(
            "AdvView: typeId", str(device.system_status.advancedView.typeId)
        )

        info_table.add_row("AdvView: Kernel", device.system_status.advancedView.Kernel)
        info_table.add_row(
            "AdvView: LocalGitVersion",
            device.system_status.advancedView.LocalGitVersion,
        )
        info_table.add_row(
            "AdvView: RemoteGitVersion",
            device.system_status.advancedView.RemoteGitVersion,
        )
        info_table.add_row(
            "AdvView: UpgradeSource", device.system_status.advancedView.UpgradeSource
        )
        info_table.add_row(
            "AdvView: IPs", ", ".join(device.system_status.advancedView.IPs)
        )
    info_table.add_section()
    if device.system_status.advancedView.Utilization:
        info_table.add_row(
            "AdvView: Utilization: CPU",
            f"{device.system_status.advancedView.Utilization.CPU:.2f}%",
        )
        info_table.add_row(
            "AdvView: Utilization: Memory",
            f"{device.system_status.advancedView.Utilization.Memory:.2f}%",
        )
        info_table.add_row(
            "AdvView: Utilization: Uptime",
            device.system_status.advancedView.Utilization.Uptime,
        )

    info_table.add_section()
    if device.playlists:
        info_table.add_row(
            "playlists: Names", str([playlist.name for playlist in device.playlists])
        )

    console.print(info_table)


@cli.command("scan")
async def command_scan() -> None:
    """Scan for FPP devices on the network."""
    zeroconf = AsyncZeroconf()
    background_tasks = set()

    table = Table(
        title="\n\nFound FPP devices", header_style="cyan bold", show_lines=True
    )
    table.add_column("Addresses")
    table.add_column("MAC Address")

    def async_on_service_state_change(
        zeroconf: Zeroconf,
        service_type: str,
        name: str,
        state_change: ServiceStateChange,
    ) -> None:
        """Handle service state changes."""
        if state_change is not ServiceStateChange.Added:
            return

        future = asyncio.ensure_future(
            async_display_service_info(zeroconf, service_type, name)
        )
        background_tasks.add(future)
        future.add_done_callback(background_tasks.discard)

    async def async_display_service_info(
        zeroconf: Zeroconf, service_type: str, name: str
    ) -> None:
        """Retrieve and display service info."""
        info = AsyncServiceInfo(service_type, name)
        await info.async_request(zeroconf, 3000)
        if info is None:
            return

        console.print(f"[cyan bold]Found service {info.server}: is a FPP device 🎉")

        table.add_row(
            f"{str(info.server).rstrip('.')}\n"
            + ", ".join(info.parsed_scoped_addresses())
        )

    console.print("[green]Scanning for FPP devices...")
    console.print("[red]Press Ctrl-C to exit\n")

    with Live(table, console=console, refresh_per_second=4):
        browser = AsyncServiceBrowser(
            zeroconf.zeroconf,
            "_fppd._udp.local.",
            handlers=[async_on_service_state_change],
        )

        try:
            forever = asyncio.Event()
            await forever.wait()
        except KeyboardInterrupt:
            pass
        finally:
            console.print("\n[green]Control-C pressed, stopping scan")
            await browser.async_cancel()
            await zeroconf.async_close()


if __name__ == "__main__":
    cli()
