import json
import logging
import sys

import geoip2.database

log = logging.getLogger("geoip_city")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)

misperrors = {"error": "Error"}
mispattributes = {"input": ["ip-src", "ip-dst", "domain|ip"], "output": ["freetext"]}
moduleconfig = ["local_geolite_db"]
# possible module-types: 'expansion', 'hover' or both
moduleinfo = {
    "version": "0.1",
    "author": "GlennHD",
    "description": (
        "An expansion module to query a local copy of Maxmind's Geolite database with an IP address, in order to get"
        " information about the city where it is located."
    ),
    "module-type": ["expansion", "hover"],
    "name": "GeoIP City Lookup",
    "logo": "maxmind.png",
    "requirements": ["A local copy of Maxmind's Geolite database"],
    "features": (
        "The module takes an IP address attribute as input and queries a local copy of the Maxmind's Geolite database"
        " to get information about the city where this IP address is located."
    ),
    "references": ["https://www.maxmind.com/en/home"],
    "input": "An IP address MISP attribute.",
    "output": "Text containing information about the city where the IP address is located.",
}


def handler(q=False):
    if q is False:
        return False
    request = json.loads(q)

    if not request.get("config") or not request["config"].get("local_geolite_db"):
        return {"error": "Please specify the path of your local copy of Maxminds Geolite database"}
    path_to_geolite = request["config"]["local_geolite_db"]

    if request.get("ip-dst"):
        toquery = request["ip-dst"]
    elif request.get("ip-src"):
        toquery = request["ip-src"]
    elif request.get("domain|ip"):
        toquery = request["domain|ip"].split("|")[1]
    else:
        return False

    try:
        reader = geoip2.database.Reader(path_to_geolite)
    except FileNotFoundError:
        return {"error": f"Unable to locate the GeoLite database you specified ({path_to_geolite})."}
    log.debug(toquery)
    try:
        answer = reader.city(toquery)
        stringmap = (
            "Continent="
            + str(answer.continent.name)
            + ", Country="
            + str(answer.country.name)
            + ", Subdivision="
            + str(answer.subdivisions.most_specific.name)
            + ", City="
            + str(answer.city.name)
        )

    except Exception as e:
        misperrors["error"] = f"GeoIP resolving error: {e}"
        return misperrors

    r = {"results": [{"types": mispattributes["output"], "values": stringmap}]}

    return r


def introspection():
    return mispattributes


def version():
    moduleinfo["config"] = moduleconfig
    return moduleinfo
