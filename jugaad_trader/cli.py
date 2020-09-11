import os
import configparser
import pickle
import click
from .zcli import zerodha
from .ucli import upstox

cli = click.Group(commands={
                            "zerodha": zerodha,
                            "upstox": upstox
                            })



if __name__ == "__main__":
    cli()
