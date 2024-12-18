"""Models for FPP Client."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.types import SerializationStrategy


class TimedeltaSerializationStrategy(SerializationStrategy, use_annotations=True):
    """Serialization strategy for timedelta objects."""

    def serialize(self, value: timedelta) -> int:
        """Serialize timedelta object to seconds."""
        return int(value.total_seconds())

    def deserialize(self, value: int) -> timedelta:
        """Deserialize integer to timedelta object."""
        return timedelta(seconds=value)


class TimestampSerializationStrategy(SerializationStrategy, use_annotations=True):
    """Serialization strategy for datetime objects."""

    def serialize(self, value: datetime) -> float:
        """Serialize datetime object to timestamp."""
        return value.timestamp()

    def deserialize(self, value: float) -> datetime:
        """Deserialize timestamp to datetime object."""
        return datetime.fromtimestamp(value, tz=UTC)


class BaseModel(DataClassORJSONMixin):
    """Base model for all FPP models."""

    # pylint: disable-next=too-few-public-methods
    class Config(BaseConfig):
        """Mashumaro configuration."""

        omit_none = True
        serialization_strategy = {  # noqa: RUF012
            datetime: TimestampSerializationStrategy(),
            timedelta: TimedeltaSerializationStrategy(),
        }
        serialize_by_alias = True


@dataclass(kw_only=True)
class CurrentPlaylist(BaseModel):
    """Current Playlist Information.

    "current_playlist": {
      "count": "4",
      "description": "Full Test 1",
      "index": "2",
      "playlist": "Test1",
      "type": "pause"
    },
    """

    count: int = 0
    description: str = ""
    index: int = 0
    playlist: str = ""
    type: str = ""


@dataclass(kw_only=True)
class MQTTStatus(BaseModel):
    """MQTT Status."""

    configured: bool = False
    connected: bool = False

@dataclass(kw_only=True)
class SystemStatusAdvanceViewUtilization(BaseModel):
    """Advanced system status information."""

    CPU: float = 0.0
    Memory: float = 0.0
    Uptime: str = ""


@dataclass(kw_only=True)
class SystemStatusAdvanceView(BaseModel):
    """Advanced system status information."""

    HostName: str = ""
    HostDescription: str = ""
    Platform: str = ""
    Variant: str = ""
    Mode: str = ""
    Version: str = ""
    Branch: str = ""
    OSVersion: str = ""
    OSRelease: str = ""
    channelRanges: str = ""
    majorVersion: int = 0
    minorVersion: int = 0
    typeId: int = 0
    Utilization: SystemStatusAdvanceViewUtilization = field(default_factory=SystemStatusAdvanceViewUtilization)
    Kernel: str = ""
    LocalGitVersion: str = ""
    RemoteGitVersion: str = ""
    UpgradeSource: str = ""
    IPs: list[str] = field(default_factory=list)


@dataclass(kw_only=True)
class SystemStatus(BaseModel):  # pylint: disable=too-many-instance-attributes
    """Object holding information from FPP.

    Json representation:
    ```json
          "endpoint": "system/status",
      "methods": {
        "GET": {
          "desc": "Gives a fppd, network, current playlist, schedule, utilization, host, version, and mqtt information.  Can also pass an optional array of ip addresses like &ip[]=192.168.0.1&ip[]=192.168.0.2 to get information on a remote.",
          "output": {
            "MQTT": {
              "configured": true,
              "connected": true
            },
            "current_playlist": {
              "count": "4",
              "description": "Full Test 1",
              "index": "2",
              "playlist": "Test1",
              "type": "pause"
            },
            "current_sequence": "",
            "current_song": "",
            "fppd": "running",
            "mode": 2,
            "mode_name": "player",
            "next_playlist": {
              "playlist": "Test3",
              "start_time": "Sun @ 17:00:00 - (Everyday)"
            },
            "repeat_mode": 1,
            "scheduler": {
              "currentPlaylist": {
                "actualEndTime": 1613365200,
                "actualEndTimeStr": "Mon @ 00:00:00",
                "actualStartTime": 1613314804,
                "actualStartTimeStr": "Sun @ 10:00:04",
                "currentTime": 1613314842,
                "currentTimeStr": "Wed @ 19:00:00",
                "playlistName": "Test1",
                "scheduledEndTime": 1613365200,
                "scheduledEndTimeStr": "Mon @ 00:00:00",
                "scheduledStartTime": 1613278800,
                "scheduledStartTimeStr": "Sun @ 00:00:00",
                "secondsRemaining": 50358,
                "stopType": 0,
                "stopTypeStr": "Graceful"
              },
              "enabled": 1,
              "nextPlaylist": {
                "playlistName": "Test3",
                "scheduledStartTime": 0,
                "scheduledStartTimeStr": "Sun @ 17:00:00 - (Everyday)"
              },
              "status": "playing"
            },
            "seconds_elapsed": "5",
            "seconds_played": "5",
            "seconds_remaining": "7",
            "status": 1,
            "status_name": "playing",
            "time": "Sun Feb 14 10:00:42 EST 2021",
            "time_elapsed": "00:05",
            "time_remaining": "00:07",
            "uptime": "00:38",
            "uptimeDays": 0.0004398148148148148,
            "uptimeHours": 0.010555555555555556,
            "uptimeMinutes": 0.6333333333333333,
            "uptimeSeconds": 38,
            "uptimeStr": "0 days, 0 hours, 0 minutes, 38 seconds",
            "uptimeTotalSeconds": 38,
            "volume": 70,
            "wifi": [],
            "interfaces": [
              {
                "ifindex": 1,
                "ifname": "lo",
                "flags": ["LOOPBACK", "UP", "LOWER_UP"],
                "mtu": 65536,
                "qdisc": "noqueue",
                "operstate": "UNKNOWN",
                "group": "default",
                "txqlen": 1000,
                "addr_info": [
                  {
                    "family": "inet",
                    "local": "127.0.0.1",
                    "prefixlen": 8,
                    "scope": "host",
                    "label": "lo",
                    "valid_life_time": 4294967295,
                    "preferred_life_time": 4294967295
                  }
                ]
              },
              {
                "ifindex": 2,
                "ifname": "eth0",
                "flags": [
                  "BROADCAST",
                  "MULTICAST",
                  "DYNAMIC",
                  "UP",
                  "LOWER_UP"
                ],
                "mtu": 1500,
                "qdisc": "mq",
                "operstate": "UP",
                "group": "default",
                "txqlen": 1000,
                "addr_info": [
                  {
                    "family": "inet",
                    "local": "192.168.1.149",
                    "prefixlen": 24,
                    "broadcast": "192.168.1.255",
                    "scope": "global",
                    "dynamic": true,
                    "label": "eth0",
                    "valid_life_time": 7096,
                    "preferred_life_time": 7096
                  }
                ]
              }
            ],
            "advancedView": {
              "HostName": "FPPdev",
              "HostDescription": "",
              "Platform": "Debian",
              "Variant": "Debian",
              "Mode": "player",
              "Version": "4.x-master-914-gebda8520",
              "Branch": "master",
              "OSVersion": "v3.0",
              "OSRelease": "Debian GNU/Linux 10 (buster)",
              "channelRanges": "0-103",
              "majorVersion": 4,
              "minorVersion": 1000,
              "typeId": 1,
              "Utilization": {
                "CPU": 1.8711392041373358,
                "Memory": 16.75084348563166,
                "Uptime": "6 days"
              },
              "Kernel": "4.19.0-6-amd64",
              "LocalGitVersion": "6e043d6",
              "RemoteGitVersion": "6e043d6",
              "UpgradeSource": "github.com",
              "IPs": ["192.168.1.149"]
            }
          }
        }
      }
    },
    ```
    """

    MQTT: MQTTStatus = field(default_factory=MQTTStatus)
    fppd: str = ""
    mode: int = 0
    mode_name: str = ""
    status_name: str = ""
    volume: int = field(default=0, metadata=field_options(alias="volume"))
    current_sequence: str = ""
    current_song: str = ""
    current_playlist: CurrentPlaylist = field(default_factory=CurrentPlaylist)
    seconds_played: int = 0
    seconds_elapsed: int = 0
    seconds_remaining: int = 0
    repeat_mode: int = 0
    advancedView: SystemStatusAdvanceView = field(default_factory=SystemStatusAdvanceView)


# TODO: /api/playlists/playable

@dataclass(kw_only=True)
class Sequence(BaseModel):
    """Sequence information."""

    name: str = ""

@dataclass(kw_only=True)
class PlaylistItem(BaseModel):
    """Playlist Item information."""

    type: str = ""
    enabled: int = 0
    playOnce: int = 0
    sequenceName: str =""
    mediaName: str =""
    videoOut: str=""
    timecode: str=""
    duration:float	= 220.025

@dataclass(kw_only=True)
class Playlist(BaseModel):
    """Playlist information."""

    name: str =""
    version:	int = 0
    repeat:int= 0
    loopCount: int= 0
    empty: bool = False
    desc: str = ""
    random: int =0
    leadIn: list = field(default_factory=list)
    mainPlaylist: list[PlaylistItem] = field(default_factory=list)



@dataclass(kw_only=True)
class Device(BaseModel):
    """Object holding all information of FPP."""

    system_status: SystemStatus
    playlists: list[Playlist]
    sequences: list[Sequence]

    @classmethod
    def __pre_deserialize__(cls, d: dict[Any, Any]) -> dict[Any, Any]:
        """Pre deserialize hook for Device object."""
        if _playlists := d.get("playlists"):
            d["playlists"] = [
                {"name": name}
                for name in _playlists
            ]
        if _sequences := d.get("sequences"):
            d["sequences"] = [
                {"name": name}
                for name in _sequences
            ]
        return d

    def update_from_dict(self, data: dict[str, Any]) -> Device:
        """Return Device object from FPP API response.

        Args:
        ----
            data: Update the device object with the data received from a
                FPP device API.

        Returns:
        -------
            The updated Device object.

        """
        if _system_status := data.get("system_status"):
            self.system_status = SystemStatus.from_dict(_system_status)

        if _playlists := data.get("playlists"):
            self.playlists = [Playlist.from_dict(playlist) for playlist in _playlists]

        if _sequences := data.get("sequences"):
            self.sequences = [Sequence.from_dict(sequence) for sequence in _sequences]

        return self


