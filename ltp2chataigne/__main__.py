from config import *
from gui import *
from lighttoys_parser import open_ltp
from chataigne_project import *
from track import create_tracks, filter_by_name, add_dmx_channels
from utils import change_path_to_script_dir, make_path_if_not_exists, remove_dir
import os

change_path_to_script_dir()

# cache and config
last_ltp_path, all_configs = load_cache()

# get ltp path
ltp_path = gui_ltp_path(last_ltp_path)
project_name = os.path.basename(ltp_path).split('.')[0]
output_path = f"{os.path.dirname(ltp_path)}"
tmp_path = "tmp/"

make_path_if_not_exists(tmp_path)
make_path_if_not_exists(output_path)

project_config = all_configs.get(ltp_path, {})

# open ltp project
ltp = open_ltp(ltp_path, tmp_path)
print("Project opened.")

# match tracks with devices
tracks = ltp["tracks"]
start_time = ltp["solution"]["start"]

project_config = gui_select_tracks(tracks, start_time, project_config)

track_selection = project_config["tracks"]
chataigne_base_path = project_config["chataigneProjectPath"]
start_time = project_config["startTime"]

all_configs.update({ltp_path: project_config})


time_shift = -start_time
tracks = create_tracks(ltp, time_shift)
tracks = filter_by_name(tracks, track_selection)
tracks = add_dmx_channels(tracks, track_selection)

if len(tracks) > 0:
    converter = ChataigneProject(tracks, chataigne_base_path)
    exported_json = converter.generate_projects_json()

    path = f"{output_path}/{project_name}.noisette"

    with open("%s" % path, 'w') as f:
        f.write(exported_json)

    print("Exported to " + path)

# save cache
save_cache(ltp_path, all_configs)

# cleanup
remove_dir(tmp_path)

print("All done.")
