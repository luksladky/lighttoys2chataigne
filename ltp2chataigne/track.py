from lighttoys_parser import *


@dataclass
class Track:
    elements: List[Element]
    name: str
    total_time: int
    dmx_channel: int = -1

def filter_by_name(tracks: List[Track], filter:dict):
    return [t for t in tracks
            if t.name in filter
            and filter[t.name]["include"]]

def add_dmx_channels(tracks: List[Track], bindings:dict):
    for t in tracks:
        t.dmx_channel = bindings[t.name]["dmx"]

    return tracks

def create_tracks(ltp, time_shift=0):
    tracks = []

    for t in ltp["tracks"]:
        elements = make_elements_from_ltp(t["elements"])
        elements = offset_by(elements, time_shift)
        elements = fill_space_with_black(elements)
        elements = fill_to_end(elements, ltp["solution"]["end"])
        tracks += [Track(elements, t["name"], ltp["solution"]["end"] + time_shift)]

    return tracks
