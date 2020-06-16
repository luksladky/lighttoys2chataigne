import json
from tqdm import tqdm

from elements import *
from track import Track
from typing import List


class ChataigneProject:
    def __init__(self, tracks: List[Track], chataigne_merge_file: str = "", prefix="", suffix="") -> None:
        self.chataigne_merge_file = chataigne_merge_file
        self.tracks = tracks
        self.prefix = prefix
        self.suffix = suffix
        self.total_time = chataigne_time(tracks[0].total_time)

    def generate_projects_json(self) -> str:
        tracks = self._generate_tracks()

        return self._generate_solution_json(tracks)

    def _generate_tracks(self) -> List:
        track_jsons = []
        for i, track in enumerate(tqdm(self.tracks)):
            track.name = self.prefix + track.name + self.suffix
            track_jsons.append(self._get_track_json(track))

        return track_jsons

    def _generate_solution_json(self, all_tracks: List) -> str:
        solution = self._get_solution(all_tracks)
        return json.dumps(solution, sort_keys=False, separators=(', ', ': '))

    def _get_metadata(self) -> dict:
        return {
            "version": "1.6.14",
            "versionNumber": 67078
        }

    def _get_dmx_module(self):
        return {
                    "niceName": "DMX",
                    "type": "DMX",
                    "scripts": {},
                    "params": {
                        "containers": {
                            "openDMX": {}
                        }
                    },
                    "values": {
                        "editorIsCollapsed": True
                    },
                    "device": {}
                }


    def _get_dmx_output(self, start_channel: int):
        if start_channel is None:
            return {}

        return {
            "items": [
                {
                    "niceName": "MappingOutput",
                    "type": "BaseItem",
                    "commandModule": "dmx",
                    "commandPath": "",
                    "commandType": "Set Color",
                    "command": {
                        "parameters": [
                            {
                                "value": start_channel,
                                "hexMode": False,
                                "controlAddress": "/startChannel"
                            },
                            {
                                "value": [
                                    0.0,
                                    0.0,
                                    0.0,
                                    1.0
                                ],
                                "controlAddress": "/color"
                            }
                        ]
                    }
                }
            ]
        }

    def _get_color(self, name, color: Color, start_time, interpolated: bool) -> dict:
        params = [{
            "value": float(start_time),
            "controlAddress": "/time"
        },
            {
                "value": [
                    *color,
                    1.0
                ],
                "controlAddress": "/color"
            }]
        if not interpolated:
            params += [{
                "value": "None",
                "controlAddress": "/interpolation"
            }]

        return {
            "parameters": params,
            "niceName": name,
            "type": "BaseItem"
        }

    def _get_colors(self, elements: List[Element]):
        colors = []
        last_color = Color(COL_BLACK)
        i = 0
        for element in elements:
            marks = element.get_colors()

            if last_color == element.left_edge() and len(colors) > 0:
                colors.pop()

            for mark in marks:
                colors += [self._get_color("c " + str(i), mark.color, mark.chataigne_time(), mark.interpolated)]
                i += 1

            last_color = element.right_edge()
        return colors

    def _get_mapping_dmx(self, layer_address, channel):
        return {
            "parameters": [
                {
                    "value": [
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ],
                    "controlAddress": "/outValue"
                }
            ],
            "niceName": f"{layer_address} ch:{channel}",
            "editorIsCollapsed": True,
            "type": "Mapping",
            "input": {
                "parameters": [
                    {
                        "value": f"/sequences/videoExport/layers/{layer_address}/value",
                        "controlAddress": "/inputValue"
                    }
                ]
            },
            "filters": {},
            "outputs": {
                "items": [
                    {
                        "niceName": "MappingOutput",
                        "type": "BaseItem",
                        "commandModule": "dmx",
                        "commandPath": "",
                        "commandType": "Set Color",
                        "command": {
                            "parameters": [
                                {
                                    "value": channel,
                                    "hexMode": False,
                                    "controlAddress": "/startChannel"
                                },
                                {
                                    "value": [
                                        0.0,
                                        0.0,
                                        0.0,
                                        1.0
                                    ],
                                    "controlAddress": "/color"
                                }
                            ]
                        }
                    }
                ]
            }
        }

    def _get_track_json(self, track: Track):
        return {
            "parameters": [
                {
                  "value": 18.0,
                  "controlAddress": "/listSize"
                },
                {
                  "value": 50,
                  "hexMode": False,
                  "controlAddress": "/uiHeight"
                },
                {
                  "value": [
                    0.2117647081613541,
                    0.2117647081613541,
                    0.2117647081613541,
                    1.0
                  ],
                  "controlAddress": "/layerColor"
                },
                {
                  "value": [
                    0.0,
                    0.501960813999176,
                    0.0,
                    1.0
                  ],
                  "controlAddress": "/value"
                }
              ],
            "niceName": track.name,
            "type": "Color",
            "mapping": {
                "parameters": [
                    {
                        "value": [
                            0.0,
                            0.0,
                            0.0,
                            1.0
                        ],
                        "controlAddress": "/outValue"
                    }
                ],
                "niceName": "Mapping",
                "type": "Mapping",
                "input": {
                    "parameters": [
                        {
                            "value": "",
                            "controlAddress": "/inputValue"
                        }
                    ]
                },
                "filters": {},
                "outputs": self._get_dmx_output(track.dmx_channel)
            },
            "colors": {
                "editorIsCollapsed": True,
                "items": self._get_colors(track.elements)
            },
            "recorder": {
                "parameters": [
                    {
                        "value": False,
                        "controlAddress": "/isRecording"
                    }
                ]
            }
        }

    def _get_solution(self, tracks: List[Track]) -> str:
        if self.chataigne_merge_file != "":
            with open(self.chataigne_merge_file, 'r') as json_file:
                solution = json.load(json_file)
        else:
            solution = {"metaData": self._get_metadata(),
                        "modules": {
                            "items": []
                        },
                        "states": {
                            "items": []
                        },
                        "sequences": {
                            "items": []
                        }
                        }

        solution = self._set_metadata(solution)
        solution = self._append_modules(solution)
        solution = self._append_sequence(solution, tracks)

        return solution

    def _get_sequence(self, tracks):
        return {
            "parameters": [
                {
                    "value": float(len(tracks)),
                    "controlAddress": "/listSize"
                },
                {
                    "value": float(self.total_time),
                    "controlAddress": "/totalTime"
                },
                {
                    "value": 0.0,
                    "controlAddress": "/viewStartTime"
                }
            ],
            "niceName": "CONVERTED from ltp",
            "type": "BaseItem",
            "layers": {
                "items": tracks
            },
        }

    def _set_metadata(self, solution):
        solution["metaData"] = self._get_metadata()
        return solution

    def _append_modules(self, solution):
        if not "modules" in solution: solution["modules"] = {"items": []}
        solution["modules"]["items"].append(self._get_dmx_module())
        return solution

    def _append_sequence(self, solution, tracks):
        if not "sequences" in solution: solution["sequences"] = {"items": []}
        solution["sequences"]["items"].append(self._get_sequence(tracks))
        return solution
