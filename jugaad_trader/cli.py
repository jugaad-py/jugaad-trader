import os
import configparser
import pickle
import click
from .zcli import zerodha


cli = click.Group(commands={"zerodha": zerodha})



if __name__ == "__main__":
    cli()