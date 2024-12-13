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

import click

from utils.devmode import restore_devmode, enable_devmode

@click.command()
@click.argument('source', type=click.Path(exists=True, file_okay=False, writable=True))
def devmode(source: str):
    """
    Replaces some script values with lower numbers or restores them to original from cache if devmode is already enabled.
    Script values to be changed:
    - def_research.lua for all races, except evo and random, Cost and Time values.
    - ships files, buildCost and buildTime.
    - subs files, costToBuild, timeToBuild.
    """
    cache_file = os.path.join(source, ".crm-devmode-cache")
    if os.path.exists(cache_file):
        print(f"DevMode is enabled for {source}. Restoring from cache and disabling.")
        restore_devmode(source)
    else:
        print(f"DevMode is disabled for {source}. Applying DevMode.")
        enable_devmode(source)
