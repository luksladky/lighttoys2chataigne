import json
from zipfile import ZipFile

from elements import *


def open_ltp(path, tmp_path):
    with ZipFile(path, 'r') as myzip:
        myzip.extractall(tmp_path)
    with open(f"{tmp_path}project.lt3", "r") as file:
        ltp = json.load(file)
    return ltp


def make_element_from_ltp(element: dict):
    ltp_elem_type = element["type"]
    start_time = element["startTime"]
    end_time = element["endTime"]

    # solid element
    if ltp_elem_type == 2:
        color = ltp_color2color(element["color"])
        return SolidElement(start_time, end_time, color)

    # gradient element
    if ltp_elem_type == 3:
        start_color = ltp_color2color(element["colorStart"])
        end_color = ltp_color2color(element["colorEnd"])
        return GradientElement(start_time, end_time, start_color, end_color)

    # flash element
    if ltp_elem_type == 4:
        start_color = ltp_color2color(element["colorStart"])
        end_color = ltp_color2color(element["colorEnd"])
        period = element["period"]
        ratio = element["ratio"]
        return FlashElement(start_time, end_time, start_color, end_color, period, ratio)

    # rainbow element
    if ltp_elem_type == 5:
        start_color = ltp_color2color(element["colorStart"])
        period = element["period"]
        return RainbowElement(start_time, end_time, start_color, period)

    return SolidElement(start_time, end_time, COL_BLACK)


def make_elements_from_ltp(ltp_elements: list):
    if ltp_elements is None: return []

    return [make_element_from_ltp(element) for element in ltp_elements]


def get_image_paths(ltp_images, temp_path):
    if ltp_images is None:
        return {}

    dict = {}
    for image in ltp_images:
        id = image['id']
        path = f"{temp_path}images/{image['name']}"
        dict[id] = path
    return dict


def fill_space_with_black(elements):
    result = []
    prev_end = 0
    for e in elements:
        if e.start_time != prev_end:
            result.append(SolidElement(prev_end, e.start_time - prev_end, COL_BLACK))
        result.append(e)
        prev_end = e.end_time
    return result


def fill_to_end(elements, sequence_end):
    if elements:
        last_end = elements[-1].end_time
    else:
        last_end = 0

    if last_end < sequence_end:
        elements.append(SolidElement(last_end, sequence_end - last_end, COL_BLACK))
    return elements


def offset_by(elements, time):
    for e in elements:
        e.offset(time)

    elements = [e for e in elements if e.duration > 0]
    return elements


def _clean_element_data(element: dict) -> dict:
    del element['id']
    del element['startTime']
    del element['endTime']
    del element['scale']
    del element['spacing']
    return element
