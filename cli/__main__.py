import click

from modules.devmode import devmode

@click.group()
def cli():
    pass

cli.add_command(devmode)

if __name__ == "__main__":
    cli()
