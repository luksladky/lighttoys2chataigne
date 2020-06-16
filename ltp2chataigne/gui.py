from typing import Tuple, List
import re
import PySimpleGUIQt as sg


def gui_ltp_path(last_ltp_path):
    layout = [[sg.Text('Lighttoys project:')],
              [sg.Input(last_ltp_path, key='-PATH-'), sg.FileBrowse()],

              [sg.Submit('Next', bind_return_key=True)]]

    window = sg.Window('Select project', layout)

    event, values = window.read()
    window.close()

    if event == None: exit()

    path = values['-PATH-']

    return path


def gui_select_tracks(tracks: List[dict], start_time: int, config: dict) -> dict:
    chataigne_path_cfg = config.get("chataigneProjectPath")
    if not chataigne_path_cfg: chataigne_path_cfg = ""

    start_time_cfg = config.get("startTime")
    if not start_time_cfg: start_time_cfg = start_time

    tracks_cfg = config.get("tracks")
    if tracks_cfg is None: tracks_cfg = {}

    layout = [[sg.Text('Chataigne base project:')],
              [sg.Input(chataigne_path_cfg, key='-CH_PATH-'), sg.FileBrowse()],
              [sg.Text('Start time'), sg.Input(default_text=start_time_cfg, key='-START_TIME-')],
              [sg.Text('Select tracks, DMX channel')]]

    for i, track in enumerate(tracks):
        track_cfg = tracks_cfg.get(track["name"])

        if track_cfg is None:
            include = False
            dmx = None
        else:
            include = track_cfg["include"]
            dmx = track_cfg["dmx"]

        if dmx is None:
            dmx = ""

        layout.append(
            [sg.Checkbox(track["name"], default=include, key=f"-TRACK_{i}-"), sg.Input(dmx, key=f"-DMX_{i}-")])

    layout.append([sg.Submit("Convert selected tracks!", bind_return_key=True)])

    window = sg.Window('Select DMX tracks', layout)

    event, values = window.read()
    window.close()

    if event == None: exit()

    start_time_cfg = re.sub('[^0-9]', '', values["-START_TIME-"])
    start_time_cfg = int(start_time_cfg) if start_time_cfg else start_time

    config = {"chataigneProjectPath": values["-CH_PATH-"],
              "startTime": start_time_cfg,
              "tracks": {}}

    for i, track in enumerate(tracks):
        checked = values[f'-TRACK_{i}-']
        dmx = re.sub('[^0-9]', '', values[f'-DMX_{i}-'])
        dmx = int(dmx) if dmx else None
        config["tracks"][track["name"]] = {"include": checked, "dmx": dmx}

    return config
