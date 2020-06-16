import os
import yaml

CACHE_PATH = "cache.yaml"

def create_default_cache():
    cache = {"lastLtpPath": '', "bindings": {}}

    with open(CACHE_PATH, 'w') as file:
        file.write(yaml.dump(cache, Dumper=yaml.Dumper))

    return cache


def load_cache():
    if not os.path.isfile(CACHE_PATH):
        create_default_cache()

    with open(CACHE_PATH, 'r') as ymlfile:
        cache = yaml.load(ymlfile, Loader=yaml.Loader)
    last_ltp_path = cache["lastLtpPath"]
    bindings = cache["bindings"] if cache["bindings"] else {}

    return last_ltp_path, bindings


def save_cache(ltp_path, bindings):
    cache = {"lastLtpPath": ltp_path, "bindings": bindings}
    with open(CACHE_PATH, 'w') as file:
        file.write(yaml.dump(cache, Dumper=yaml.Dumper))


if __name__ == '__main__':
    cache = load_cache()
    print(cache)
