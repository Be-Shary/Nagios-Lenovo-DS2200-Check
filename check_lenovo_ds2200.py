#!/usr/bin/python

"""
ver 0.9

requirements:
    pip install paramiko

tested on:
    Python (2.7.6 && 3.9.5)
    Lenovo ThinkSystem DS2200 - ver. GT280R008-04
    Ubuntu 20.04
    CentOS (7.0 && 8.0)

todo:
    done -> add try, exception - save execute and read files and line
    done -> add read parameters form line
    done -> add help info and others hints
    done -> add port options
    dont -> remove tmp file, do math in memory
    done -> add more checks ;)
    will see -> add perfdata for some checks \_(oo)_/
    ohh god no -> organize code... -> eee maybe someday
"""

import sys, getopt, paramiko


def show_help():
    print("\nUsage: " + sys.argv[0] + " -H [host adress] -u [ssh user name] -p [ssh user password] -P [SSH port, its options, default is 22] -c [one check form list]\n")
    print("Checks: " + str(check_list) + "\n")
    print("Example: " + sys.argv[0] + " -H 100.100.0.10 -u monitor -p 'qwerty123' -P 666 -c disks\n")
    print("Example: " + sys.argv[0] + " -H 192.168.1.15 -u nagios -p 'p@ssw0rd' -c psu\n")
    print("WARNING! Password must be between '<---->' if you have special char like $ in it!")
    sys.exit(UNKNOWN)


def show_data():
    if check == "disks":
        for i in range(0, len(disks), 3):
            print(disks[i] + " - " + disks[i + 1] + " - " + disks[i + 2])
    elif check == "psu":
        for i in range(0, len(psu), 6):
            print(psu[i] + " - " + psu[i + 1] + " ; " + psu[i + 2] + " - " + psu[i + 3] + " ; " + psu[i + 4] + " -  " +
                  psu[i + 5])
    elif check == "disk-groups":
        for i in range(0, len(groups), 4):
            print("Disk groups: " + groups[i] + " - Size of: " + groups[i + 1] + " / Free space:" + groups[
                i + 2] + " - " + groups[i + 3])
    elif check == "pools":
        for i in range(0, len(pools), 8):
            print("Pool name: " + pools[i] + " - Total Size: " + pools[i + 1] + " / Available: " + pools[
                i + 2] + " - Rebalance: " + pools[i + 3] + " - " + pools[i + 4])
    elif check == "init":
        for i in range(0, len(init), 6):
            print("Nickname: " + init[i] + " / Discovered: " + init[i + 1] + " / Mapped: " + init[
                i + 2] + " / Profile: " + init[i + 3] + " / Host: " + init[i + 4] + " / ID: " + init[i + 5])
            if init[i + 1] == "NO" or init[i + 2] == "NO":
                sys.exit(WARNING)
    elif check == "sensors":
        for i in range(0, len(sensors), 2):
            print(sensors[i] + " - " + sensors[i + 1])
    elif check == "controllers":
        for i in range(0, len(controllers), 3):
            print(controllers[i] + " - " + controllers[i + 1] + " - " + controllers[i + 2])
    elif check == "enclosures":
        for i in range(0, len(enclosures), 2):
            print(enclosures[i] + " - " + enclosures[i + 1])
    else:
        print("Something went wrong...?")
        sys.exit(UNKNOWN)


def get_data(command):
    global check
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=user, password=password, timeout=30)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read()
        tmp = output.split()
        ssh.close()
        del ssh, stdin, stdout, stderr
        return tmp

    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
        sys.exit(UNKNOWN)
    except paramiko.SSHException, e:
        print(e)
        print("Unable to establish SSH connection.")
        sys.exit(UNKNOWN)


# some variables
global check
disks = []
psu = []
groups = []
pools = []
init = []
sensors = []
controllers = []
enclosures = []
tmp = []
host = None
user = None
password = None
check = None
flag = False
port = 22  # default number if not user add
check_list = ("disks", "psu", "disk-groups", "pools", "init", "sensors", "controllers", "enclosures")

# nagios return codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

# read command line arguments
try:
    optlist, args = getopt.getopt(sys.argv[1:], 'hH:u:p:P:c:')
except getopt.GetoptError:
    show_help()
    sys.exit(UNKNOWN)

for opt, arg in optlist:
    if opt == '-h':
        show_help()
        sys.exit(UNKNOWN)
    if opt == '-H':
        host = str(arg)
    if opt == "-u":
        user = str(arg)
    if opt == "-p":
        password = str(arg)
    if opt == "-P":
        port = int(arg)
    if opt == '-c':
        check = str(arg)

if host == None or user == None or password == None or check == None:
    show_help()
    sys.exit(UNKNOWN)
if not check in check_list:
    show_help()
    sys.exit(UNKNOWN)

# do the magic
if check == "disks":
    tmp = get_data("show disks")
    try:
        for i in range(len(tmp)):
            if str(tmp[i]).find('name="slot"') >= 0:
                disks.append("Slot: " + str(tmp[i + 5].split(">")[1].split("<")[0]))
            elif str(tmp[i]).find('name="serial-number"') >= 0:
                disks.append("Serial: " + str(tmp[i + 6].split(">")[1].split("<")[0]))
            elif str(tmp[i]).find('name="health"') >= 0:
                if str(tmp[i + 5].split(">")[1].split("<")[0]) == "OK":
                    disks.append("Status: OK")
                else:
                    disks.append("Status: ERROR")
                    flag = True
    except IndexError:
        print("Ops... there is problem with data...")
        sys.exit(UNKNOWN)

    if len(disks) == 0:
        print("CRITICAL - didn't get right data")
        sys.exit(CRITICAL)
    if flag:
        print("CRITICAL - some disk(s) are not healthy")
        show_data()
        sys.exit(CRITICAL)
    else:
        print("OK - All " + str(len(disks) / 3) + " disk(s) are fine - check data.")
        show_data()
        sys.exit(OK)

if check == "psu":
    tmp = get_data("show power-supplies")
    try:
        for i in range(len(tmp)):
            if str(tmp[i]).find('name="name"') >= 0:
                psu.append((tmp[i + 5] + tmp[i + 6] + tmp[i + 7]).split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="health"') >= 0:
                if str(tmp[i + 5].split(">")[1].split("<")[0]) == "OK":
                    psu.append("Status: OK")
                else:
                    psu.append("Status: ERROR")
                    flag = True
    except IndexError:
        print("Ops... there is problem with data...")
        sys.exit(UNKNOWN)

    if len(psu) == 0:
        print("CRITICAL - didn't get right data")
        sys.exit(CRITICAL)
    if flag:
        print("CRITICAL - some psu(s) are not healthy")
        show_data()
        sys.exit(CRITICAL)
    else:
        print("OK - All power units and fans are working - check data.")
        show_data()
        sys.exit(OK)

if check == "disk-groups":
    tmp = get_data("show disk-groups")
    try:
        for i in range(len(tmp)):
            if str(tmp[i]).find('name="name"') >= 0:
                groups.append(tmp[i + 5].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="size"') >= 0:
                groups.append(tmp[i + 6].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="freespace"') >= 0:
                groups.append(tmp[i + 6].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="health"') >= 0:
                if (tmp[i + 5].split(">")[1].split("<")[0]) == "OK":
                    groups.append("Status: OK")
                else:
                    groups.append("Status: ERROR")
                    flag = True
    except IndexError:
        print("Ops... there is problem with data...")
        sys.exit(UNKNOWN)

    if len(groups) == 0:
        print("CRITICAL - didn't get right data")
        sys.exit(CRITICAL)
    if flag:
        print("CRITICAL - some some problem with disks groups")
        show_data()
        sys.exit(CRITICAL)
    else:
        print("OK - Everything seems fine - check data.")
        show_data()
        sys.exit(OK)

if check == "pools":
    tmp = get_data("show pools")
    try:
        for i in range(len(tmp)):
            if str(tmp[i]).find('name="name"') >= 0:
                pools.append(tmp[i + 5].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="total-size"') >= 0:
                pools.append(tmp[i + 7].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="total-avail"') >= 0:
                pools.append(tmp[i + 6].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="rebalance"') >= 0:
                pools.append(tmp[i + 6].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="health"') >= 0:
                if (tmp[i + 5].split(">")[1].split("<")[0]) == "OK":
                    pools.append("Status: OK")
                else:
                    pools.append("Status: ERROR")
                    flag = True
    except IndexError:
        print("Ops... there is problem with data...")
        sys.exit(UNKNOWN)

    if len(pools) == 0:
        print("CRITICAL - didn't get right data")
        sys.exit(CRITICAL)
    if flag:
        print("CRITICAL - check pools")
        show_data()
        sys.exit(CRITICAL)
    else:
        print("OK - Everything looks good - check data.")
        show_data()
        sys.exit(OK)

if check == "init":
    tmp = get_data("show initiators")
    try:
        for i in range(len(tmp)):
            if str(tmp[i]).find('name="nickname"') >= 0:
                init.append(tmp[i + 5].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="discovered"') >= 0:
                init.append(tmp[i + 5].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="mapped"') >= 0:
                init.append(tmp[i + 5].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="profile"') >= 0:
                init.append(tmp[i + 5].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="host-bus-type"') >= 0:
                init.append(tmp[i + 6].split(">")[1].split("<")[0])
            elif str(tmp[i]).find('name="id"') >= 0:
                init.append(tmp[i + 6].split(">")[1].split("<")[0])
    except IndexError:
        print("Ops... there is problem with data...")
        sys.exit(UNKNOWN)

    if len(init) == 0:
        print("CRITICAL - didn't get right data")
        sys.exit(CRITICAL)

    show_data()
    sys.exit(OK)

if check == "sensors":
    tmp = get_data("show sensor-status")
    try:
        for i in range(len(tmp)):
            if str(tmp[i]).find('name="sensor-name"') >= 0:
                temp_name = []
                temp_name.append(tmp[i + 7].split(">")[1].split("<")[0])
                for n in range(1, 5):
                    if (tmp[i + 7 + n].find("<") == -1) and (tmp[i + 7 + n].find('name="value"') == -1) and tmp[
                        i + 7 + n].find('type="string"') == -1:
                        temp_name.append(tmp[i + 7 + n].split("<")[0])
                sensors.append(" ".join(temp_name))
            elif tmp[i].find('name="status"') >= 0 and tmp[i - 1].find('basetype="status"') == -1:
                if (tmp[i + 5].split(">")[1].split("<")[0]) == "OK":
                    sensors.append("Status: OK")
                else:
                    sensors.append("Status: ERROR")
                    flag = True
    except IndexError:
        print("Ops... there is problem with data...")
        sys.exit(UNKNOWN)

    if len(sensors) == 0:
        print("CRITICAL - didn't get right data")
        sys.exit(CRITICAL)

    if flag:
        print("CRITICAL - check sensors info.")
        show_data()
        sys.exit(CRITICAL)
    else:
        print("OK - All sensors are fine.")
        show_data()
        sys.exit(OK)

if check == "controllers":
    tmp = get_data("show controllers")
    try:
        for i in range(len(tmp)):
            if str(tmp[i]).find('name="durable-id"') >= 0:
                controllers.append(tmp[i + 6].split(">")[1].split("<")[0])
            elif tmp[i].find('name="health"') >= 0:
                if (tmp[i + 5].split(">")[1].split("<")[0]) == "OK":
                    controllers.append("Status: OK")
                    controllers.append("No action is required")
                elif (tmp[i + 5].split(">")[1].split("<")[0]) == "N/A":
                    controllers.append("Status: N/A")
                    controllers.append("No drive enclosure is connected to this expansion port")
                else:
                    controllers.append("Status: ERROR")
                    controllers.append("Check controller")
                    flag = True
    except IndexError:
        print("Ops... there is problem with data...")
        sys.exit(UNKNOWN)

    if len(controllers) == 0:
        print("CRITICAL - didn't get right data")
        sys.exit(CRITICAL)

    if flag:
        print("CRITICAL - check controllers info.")
        show_data()
        sys.exit(CRITICAL)
    else:
        print("OK - No action is required. Check info.")
        show_data()
        sys.exit(OK)

if check == "enclosures":
    tmp = get_data("show enclosures")
    try:
        for i in range(len(tmp)):
            if str(tmp[i]).find('name="durable-id"') >= 0:
                enclosures.append(tmp[i + 6].split(">")[1].split("<")[0])
            elif tmp[i].find('name="health"') >= 0:
                if (tmp[i + 5].split(">")[1].split("<")[0]) == "OK":
                    enclosures.append("Status: OK")
                elif (tmp[i + 5].split(">")[1].split("<")[0]) == "N/A":
                    enclosures.append("Status: N/A")
                else:
                    enclosures.append("Status: ERROR")
                    flag = True
    except IndexError:
        print("Ops... there is problem with data...")
        sys.exit(UNKNOWN)

    if len(enclosures) == 0:
        print("CRITICAL - didn't get right data")
        sys.exit(CRITICAL)

    if flag:
        print("CRITICAL - check enclosures info.")
        show_data()
        sys.exit(CRITICAL)
    else:
        print("OK - No action is required. Check info.")
        show_data()
        sys.exit(OK)
