import os
import configparser
import pickle
import click
from jugaad_trader import Zerodha
from jugaad_trader.util import CLI_NAME


app_dir = click.get_app_dir(CLI_NAME)
if not os.path.exists(app_dir):
    os.makedirs(app_dir)

cred_file = '.zcred'
session_file = '.zsession'

@click.group()
def zerodha():
    """ Command line utilities for managing Zerodha account
        Get started by creating a session

        $ jtrader zerodha startsession
    """
    pass

@zerodha.command()
def startsession():
    """Saves your login session in the app config folder"""

    user_id = click.prompt("User ID >")
    password = click.prompt("Password >", hide_input=True)
    z = Zerodha()
    z.user_id = user_id
    z.password = password
    j = z.login_step1()
    if j['status'] == 'error':
        click.echo(click.style("Error: {}".format(j['message']), fg="red"))
        return
    z.twofa = click.prompt("Pin >", hide_input=True)
    j = z.login_step2(j)
    if j['status'] == 'error':
        click.echo(click.style("Error: {}".format(j['message']), fg="red"))
        return
    z.enc_token = z.r.cookies['enctoken']
    p = z.profile()

    click.echo(click.style("Logged in successfully as {}".format(p['user_name']), fg='green'))
    with open(os.path.join(app_dir, session_file), "wb") as fp:
        pickle.dump(z.reqsession, fp)
    click.echo("Saved session successfully")

@zerodha.command()
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



@zerodha.command()
def configdir():
    """Print app config directory location"""
    click.echo(app_dir)


@zerodha.command()
@click.argument("config")
def rm(config):
    """Delete stored credentials or sessions config

        To delete SESSION

        $ jtrader zerodha rm SESSION

        To delete CREDENTIALS

        $ jtrader zerodha rm CREDENTIALS
    """
    if config == "CREDENTIALS":
        try:
            os.remove(os.path.join(app_dir, cred_file))
        except FileNotFoundError:
            click.echo("Could not find any credentials, you can save it again using 'jtrader zerodha savecreds'")
        else:
            click.echo("Successfully deleted credentials config, you can save it again using 'jtrader zerodha savecreds`")
    
    if config == "SESSION":
        try:
            os.remove(os.path.join(app_dir, session_file))
        except FileNotFoundError:
            click.echo("Could not find the session config, you can save it again using 'jtrader zerodha startsession'")
        else:
            click.echo("Successfully deleted, you can save it again using 'jtrader zerodha startsession'")
    





if __name__ == "__main__":
    zerodha()
