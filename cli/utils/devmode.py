""" This file is part of CRM-Tinkerer-CLI.

CRM-Tinkerer-CLI is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CRM-Tinkerer-CLI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with CRM-Tinkerer-CLI. If not, see <https://www.gnu.org/licenses/>. """
import os
import re
import json

import click

races = ["hiigaran", "kadeshi", "keeper", "kushan", "taiidan", "turanic", "vaygr"]

def enable_devmode(source: str):
    cache_file = os.path.join(source, ".crm-devmode-cache")
    if os.path.exists(cache_file):
        if not click.confirm(f"DevMode is enabled for {source}. Continue?", default=False):
            print("Aborting...")
            return

    cache = {}

    print("Modifying research files...")
    for race in races:
        race_dir = os.path.join(source, "scripts/races", race, "scripts")
        if not os.path.exists(race_dir):
            print(f"Directory not found: {race_dir}")
            continue

        # Traverse directories and modify research files
        for root, _, files in os.walk(race_dir):
            for file in files:
                if file == "def_research.lua":
                    file_path = os.path.normpath(os.path.join(root, file))
                    print(file_path + "...")
                    with open(file_path, "r") as file:
                        content = file.read()

                    # Regex patterns to find Cost and Time values
                    cost_pattern = re.compile(r"(?<=\bCost\s=\s)\d+")
                    time_pattern = re.compile(r"(?<=\bTime\s=\s)\d+")

                    original_costs = cost_pattern.findall(content)
                    original_times = time_pattern.findall(content)

                    if original_costs and original_times:
                        relative_path = os.path.relpath(file_path, start=os.path.dirname(cache_file))
                        cache[relative_path] = {
                            "Cost": original_costs,
                            "Time": original_times,
                        }

                    # Replace Cost and Time values with 1
                    modified_content = cost_pattern.sub("1", content)
                    modified_content = time_pattern.sub("1", modified_content)

                    with open(file_path, "w") as file:
                        file.write(modified_content)

    # Traverse ship directories and modify ship files
    ship_dir = os.path.join(source, "ship")
    print("Modifying ship files...")
    for root, _, files in os.walk(ship_dir):
        for file in files:
            if file.endswith(".ship"):
                file_path = os.path.join(root, file)
                print(file_path + "...")
                with open(file_path, "r") as ship_file:
                    content = ship_file.read()

                # Regex patterns to find buildCost and buildTime values
                build_cost_pattern = re.compile(r"(?<=NewShipType\.buildCost=)\d+")
                build_time_pattern = re.compile(r"(?<=NewShipType\.buildTime=)\d+")

                # Find and cache original values
                original_build_costs = build_cost_pattern.findall(content)
                original_build_times = build_time_pattern.findall(content)

                if original_build_costs or original_build_times:
                    relative_path = os.path.relpath(file_path, start=os.path.dirname(cache_file))
                    cache[relative_path] = {
                        "buildCost": original_build_costs,
                        "buildTime": original_build_times,
                    }

                # Replace buildCost and buildTime values with 1
                modified_content = build_cost_pattern.sub("1", content)
                modified_content = build_time_pattern.sub("1", modified_content)

                # Write modified content back to file
                with open(file_path, "w") as ship_file:
                    ship_file.write(modified_content)

    with open(cache_file, "w") as file:
        json.dump(cache, file, indent=4)

    print("Modification complete. Cache saved.")

def restore_devmode(source: str):
    cache_file = os.path.join(source, ".crm-devmode-cache")
    if not os.path.exists(cache_file):
        print("No cache file found. Nothing to restore.")
        return

    with open(cache_file, "r") as file:
        cache = json.load(file)

    for relative_path, values in cache.items():
        print("Restoring " + relative_path + "...")
        file_path = os.path.normpath(os.path.join(os.path.dirname(cache_file), relative_path))
        with open(file_path, "r") as file:
            content = file.read()

        # Restore research file values
        if "Cost" in values:
            costs = iter(values["Cost"])
            content = re.sub(r"(?<=\bCost\s=\s)1", lambda _: next(costs, "1"), content)

        if "Time" in values:
            times = iter(values["Time"])
            content = re.sub(r"(?<=\bTime\s=\s)1", lambda _: next(times, "1"), content)

        # Restore ship file values
        if "buildCost" in values:
            build_costs = iter(values["buildCost"])
            content = re.sub(r"(?<=NewShipType\.buildCost=)1", lambda _: next(build_costs, "1"), content)

        if "buildTime" in values:
            build_times = iter(values["buildTime"])
            content = re.sub(r"(?<=NewShipType\.buildTime=)1", lambda _: next(build_times, "1"), content)

        with open(file_path, "w") as file:
            file.write(content)

    os.remove(cache_file)
    print("Restoration complete. Cache file deleted.")
