import os
import configparser
import pickle
import click
from jugaad_trader import Upstox
from jugaad_trader.util import CLI_NAME


app_dir = click.get_app_dir(CLI_NAME)
if not os.path.exists(app_dir):
    os.makedirs(app_dir)

cred_file = '.ucred'
session_file = '.usession'

@click.group()
def upstox():
    """ Command line utilities for managing Upstox account
        Get started by creating a session

        $ jtrader zerodha startsession
    """
    pass

@upstox.command()
def savecreds():
    """Saves your creds in the APP config directory"""
    click.echo("Saves your creds in app config folder in file named {}".format(cred_file))
    user_id = click.prompt("User ID >")
    password = click.prompt("Password >", hide_input=True)
    twofa = click.prompt("Pin >", hide_input=True)
    config = configparser.ConfigParser()
    config['CREDENTIALS'] = {'user_id': user_id,
                                'password': password,
                                'twofa': twofa}
    with open(os.path.join(app_dir, cred_file), "w") as fp:
        config.write(fp)
        click.echo(click.style("Saved credentials successfully", fg='green'))


