# -------------------------- Modules -------------------------- #
import geocoder
import six
from pyfiglet import figlet_format 
import click
import folium
import socket
import os
import platform
import urllib.request
import webbrowser

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


    
#test ip: 161.185.160.93

# ---- Function (1): Get type of IP [current device || external device] ---- #

@click.command(add_help_option=False)
@click.option('--target_ip', default='', help="Ip Address of Target!")
@click.option('--get_my_ip_or_not', default='n', help="Use [--get_my_ip_or_not=y]: for use your Ip Address. Or [--get_my_ip_or_not=n]: for use external Ip Address!")
@click.option('-v', '--version', flag_value='version', help="Tool Version!")
@click.option('--info', flag_value='show_info', help="Get some Information about tool")
@click.help_option('--help', '-h', help='Show parameters & options you can use it!')

def main(target_ip='', get_my_ip_or_not:str = '', info='', version=''):
    if target_ip != '': # Check If user enter 'target_ip' directly
        getExternalIp(target_ip)
    elif version == 'version':
        versionOfTool()
    elif info == 'show_info':
        infoAboutTool()
    else: 
        # Start Main CLI #
        getMyIpOrNot(get_my_ip_or_not)

# ---- Function (2): Check if user wanna use him ip or another ---- #
def getMyIpOrNot(get_my_ip_or_not):
    helloMsg()
    if get_my_ip_or_not.lower() == 'n':
        targetIp = click.prompt("Enter Target Ip: ")
        getExternalIp(targetIp)
    elif get_my_ip_or_not.lower() == 'y':
        if connect():
            ip = geocoder.ip("me")
            showIpInfo(ip)
            getLocationOnMap(ip)
        else:
            textFormat("Check Network first!", color='red')
    else:
        textFormat("ERROR: Enter valid value [y or n]", color='red')        

# ---- Function (3): Get data of external device IP & show info ---- #
def getExternalIp(targetip):
    if isValidIpv4Address(targetip) or isValidIpv6Address(targetip):
        if connect():
            ip = geocoder.ip(targetip)
            showIpInfo(ip)
            getLocationOnMap(ip)
        else:
            textFormat("Check Network first!", color='red')
    else:
        textFormat("Enter Valid Ip Address!", color='red')
        getExternalIp()

# ---- Function (4): Show Tool Hello Message ---- #

def helloMsg():
    textFormat("Find Me", color="red", figlet=True)
    textFormat("Welcome to Find Me Tool for gathering information using IP!", "green")

# ---- Function (5): Show information about IP ---- #
def showIpInfo(ip):
    # -- Start Message -- #
    textFormat("--- Catched Information About IP ---", "green")
    # -- Target IP -- #
    click.secho(f"Target IP: {ip.ip}", fg='blue', bold=True)
    
    # -- City Info -- #
    city = ip.city
    click.echo(f"City: {city}")
    
    # -- latlng Info -- #
    latlng = ip.latlng
    click.echo(f"latlng: {latlng}")

# ---- Function (6): Convert normal text to -> ASCII codes ---- #
def textFormat(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)

# ---- Function (7): Convert latlng text to -> Map ---- #
def getLocationOnMap(ip):
    # Check if user wanna map
    getLocationMap = click.confirm("Do you want to show Location on Map?")
    if getLocationMap:
        location = ip.latlng
        locationMap = folium.Map(location=location, zoom_start=10)
        folium.CircleMarker(location=location, radius=50, color="red").add_to(locationMap)
        folium.Marker(location).add_to(locationMap)
        mapName = f"maps/map_{ip.ip}.html"
        locationMap.save(mapName)
        
        textFormat("Map File saved in 'maps' folder!", "green")
        
        openBrowser = click.confirm("Do you want open map in browser?")
        if openBrowser:
            ## Open map in browser ##
            absoluteURLFile = os.path.abspath(mapName)
            webbrowser.open(absoluteURLFile)
            textFormat("Map File opend in browser...", "green")
            askUserIfWannaTestAnotherIP()
        else:
            askUserIfWannaTestAnotherIP()
            
    else:
        textFormat("Map file not saved", color='red')
        askUserIfWannaTestAnotherIP()
        # textFormat("Enter valid value [y or n]", color='red')

# ---- Function (8): Check if IP (v4) is valide or not! ---- #
def isValidIpv4Address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

# ---- Function (9): Check if IP (v6) is valide or not! ---- #
def isValidIpv6Address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True

# ---- Function (10): Check if User want test another Ip or not! ---- #
def askUserIfWannaTestAnotherIP():
    useToolAgain = click.confirm("Do you want test another ip?")
    if useToolAgain:
        textFormat("OK! LET'S GO..", color='green')
        main()
    else:
        textFormat("Thank you for using IP CLI", color='green', figlet=True)
        pass


# ---- Function (11): Make Group for Information about Tool ---- #
def infoAboutTool():
    click.secho("############ Some Information about Tool ############ ", fg='blue')
    desciptionOfTool = """
Description:
    Simple CLI for get information about IP"""
    click.echo(desciptionOfTool)
    
    usageAndOptions = """
Usage:
    main.py :  Start CLI 
    main.py --target_ip
    main.py --get_my_ip_or_not
    main.py -h|--help
    main.py -v|--version

Options:
    --target_ip         Get Info from IP directly.
    --get_my_ip_or_not  Use [--get_my_ip_or_not=y]: for use your Ip Address. Or [--get_my_ip_or_not=n]: for use external Ip Address!
    -h --help           Show this screen.
    -v --version        Show version.
    """
    click.echo(usageAndOptions)

# ---- Function (12): Version Of Tool ---- #
def versionOfTool():
    textFormat("Tool Version: 1.0", color='blue')

# ---- Function (13): Check Network Status ---- #
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

if __name__ == '__main__':
    main()
