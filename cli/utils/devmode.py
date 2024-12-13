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

                    # Replace Cost and Time values with 2, only if they are not 0 or 1
                    def replace_non_zero(match):
                        if int(match.group()) > 1:
                            return "2"
                        return match.group()

                    modified_content = cost_pattern.sub(replace_non_zero, content)
                    modified_content = time_pattern.sub(replace_non_zero, modified_content)

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
                        "shipBuildCost": original_build_costs,
                        "shipBuildTime": original_build_times,
                    }

                # Replace buildCost and buildTime values with 1
                modified_content = build_cost_pattern.sub("1", content)
                modified_content = build_time_pattern.sub("1", modified_content)

                # Write modified content back to file
                with open(file_path, "w") as ship_file:
                    ship_file.write(modified_content)

    # Traverse subsystem directories and modify subs files
    subs_dir = os.path.join(source, "subsystem")
    print("Modifying subs files...")
    for root, _, files in os.walk(subs_dir):
        for file in files:
            if file.endswith(".subs"):
                file_path = os.path.join(root, file)
                print(file_path + "...")
                with open(file_path, "r") as subs_file:
                    content = subs_file.read()

                # Regex patterns to find buildCost and buildTime values
                build_cost_pattern = re.compile(r"(?<=NewSubSystemType\.costToBuild=)\d+")
                build_time_pattern = re.compile(r"(?<=NewSubSystemType\.timeToBuild=)\d+")

                # Find and cache original values
                original_build_costs = build_cost_pattern.findall(content)
                original_build_times = build_time_pattern.findall(content)

                if original_build_costs or original_build_times:
                    relative_path = os.path.relpath(file_path, start=os.path.dirname(cache_file))
                    cache[relative_path] = {
                        "subsBuildCost": original_build_costs,
                        "subsBuildTime": original_build_times,
                    }

                # Replace buildCost and buildTime values with 1
                modified_content = build_cost_pattern.sub("1", content)
                modified_content = build_time_pattern.sub("1", modified_content)

                # Write modified content back to file
                with open(file_path, "w") as subs_file:
                    subs_file.write(modified_content)

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

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}. Skipping...")
            continue

        with open(file_path, "r") as file:
            content = file.read()

        # Restore research file values
        if "Cost" in values:
            costs = iter(values["Cost"])
            def restore_cost(match):
                return next(costs, match.group())
            content = re.sub(r"(?<=\bCost\s=\s)\d+", restore_cost, content)

        if "Time" in values:
            times = iter(values["Time"])
            def restore_time(match):
                return next(times, match.group())
            content = re.sub(r"(?<=\bTime\s=\s)\d+", restore_time, content)

        # Restore ship file values
        if "shipBuildCost" in values:
            build_costs = iter(values["shipBuildCost"])
            def restore_build_cost(match):
                return next(build_costs, match.group())
            content = re.sub(r"(?<=NewShipType\.buildCost=)\d+", restore_build_cost, content)

        if "shipBuildTime" in values:
            build_times = iter(values["shipBuildTime"])
            def restore_build_time(match):
                return next(build_times, match.group())
            content = re.sub(r"(?<=NewShipType\.buildTime=)\d+", restore_build_time, content)

        # Restore subs file values
        if "subsBuildCost" in values:
            build_costs = iter(values["subsBuildCost"])
            def restore_build_cost(match):
                return next(build_costs, match.group())
            content = re.sub(r"(?<=NewSubSystemType\.costToBuild=)\d+", restore_build_cost, content)

        if "subsBuildTime" in values:
            build_times = iter(values["subsBuildTime"])
            def restore_build_time(match):
                return next(build_times, match.group())
            content = re.sub(r"(?<=NewSubSystemType\.timeToBuild=)\d+", restore_build_time, content)

        with open(file_path, "w") as file:
            file.write(content)

    os.remove(cache_file)
    print("Restoration complete. Cache file deleted.")
