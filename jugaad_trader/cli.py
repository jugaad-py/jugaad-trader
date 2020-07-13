import os
import configparser
import pickle
import click
from .zcli import zerodha

APP_NAME = 'jtrader'


cli = click.Group(commands={"zerodha": zerodha})



if __name__ == "__main__":
    cli()