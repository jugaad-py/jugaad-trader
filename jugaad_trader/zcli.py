import os
import configparser
import pickle
import click
from jugaad_trader import Zerodha, CLI_NAME

app_dir = click.get_app_dir(CLI_NAME)
if not os.path.exists(app_dir):
    os.makedirs(app_dir)



@click.group()
def zerodha():
    """Command line utilities for managin Zerodha account"""
    pass

@zerodha.command()
def savecreds():
    """Saves your creds in the APP config directory"""
    click.echo("Saves your creds in app config folder in file named .zcreds")
    user_id = click.prompt("User ID >")
    password = click.prompt("Password >", hide_input=True)
    twofa = click.prompt("Pin >", hide_input=True)
    config = configparser.ConfigParser()
    config['CREDENTIALS'] = {'user_id': user_id,
                                'password': password,
                                'twofa': twofa}
    with open(os.path.join(app_dir, '.zcreds'), "w") as fp:
        config.write(fp)
        click.echo("Saved credentials successfully")

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
        click.echo("Error: {}".format(j['message']))
        return
    z.twofa = click.prompt("Pin >", hide_input=True)
    j = z.login_step2(j)
    if j['status'] == 'error':
        click.echo("Error: {}".format(j['message']))
        return
    z.enc_token = z.r.cookies['enctoken']
    p = z.profile()

    click.echo("Logged in successfully as {}".format(p['user_name']))
    with open(os.path.join(app_dir, ".zsession"), "wb") as fp:
        pickle.dump(z.reqsession, fp)

@zerodha.command()
def configdir():
    """Print app config directory location"""
    click.echo(app_dir)

'''
@zerodha.command()
@click.argument("action")
def zerodha(action):
    """ Manage Zerodha creds

        supported actions

        $ jtrader zerodha startsession 
        
        (Preffered method) Starts a session by logging in to Zerodha account, It does not store credentials, instead stores session

        $ jtrader zerodha savecreds
        
        Saves your creds in the APP config directory  
        
        $ jtrader zerodha configdir

    """

    if action == "savecreds":
        click.echo("Saves your creds in your home folder in file named .zcreds")
        user_id = click.prompt("User ID >")
        password = click.prompt("Password >", hide_input=True)
        twofa = click.prompt("Pin >", hide_input=True)
        config = configparser.ConfigParser()
        config['CREDENTIALS'] = {'user_id': user_id,
                                    'password': password,
                                    'twofa': twofa}
        with open(os.path.join(app_dir, '.zcreds'), "w") as fp:
            config.write(fp)
            click.echo("Saved credentials successfully")
        return

    if action == "startsession":
        click.echo("Saves your login session in your home folder in file named .zsession")
        user_id = click.prompt("User ID >")
        password = click.prompt("Password >", hide_input=True)
        z = Zerodha()
        z.user_id = user_id
        z.password = password
        j = z.login_step1()
        if j['status'] == 'error':
            click.echo("Error: {}".format(j['message']))
            return
        z.twofa = click.prompt("Pin >", hide_input=True)
        j = z.login_step2(j)
        if j['status'] == 'error':
            click.echo("Error: {}".format(j['message']))
            return
        z.enc_token = z.r.cookies['enctoken']
        p = z.profile()

        click.echo("Logged in successfully as {}".format(p['user_name']))
        with open(os.path.join(app_dir, ".zsession"), "wb") as fp:
            pickle.dump(z.reqsession, fp)

        
        
'''






if __name__ == "__main__":
    zerodha()