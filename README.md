# Nagios-Lenovo-DS2200-Check
This is a simple plugin to monitor Lenovo DS2200 storage using SSH protocol.

## Overview
It was written in a hurry so I know the code is a bit messy. Maybe I'll fix it someday. For now, it works and that's enough.

## Requirements
It has been tested on:
* Python (2.7.6 && 3.9.5)
* Lenovo ThinkSystem DS2200 - ver. GT280R008-04
* Ubuntu 20.04
* CentOS (7.0 && 8.0)

It's require PARAMIKO:
`pip install paramiko`

### How it works
Plugin connect to storage via ssh and check what you need. If all health elements of check will be OK (or N/A in some cases), the nagios response will be OK (GREEN). If there will be error or fail, plug in return CRITICAL alert. Only initiators check will return warning if some problem will found.

### How to use it

 *check_lenovo_ds2200.py -H [host adress] -u [ssh user name] -p [ssh user password] -P [SSH port, its options, default is 22] -c [one form a list]*
 
 Check list: disks, psu, disk-groups, pools, init, sensors, controllers, enclosures

Example: check_lenovo_ds2200.py -H 100.100.0.10 -u monitor -p 'qwerty123' -P 666 -c disks

### Nagios configuration

First edit your nagios commands.cfg file and add:

    
    define command {
    command_name    check_lenovo_ds2200
    command_line    python $USER1$/check_lenovo_ds2200.py -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -P $ARG3$ -c $ARG4$
    }
    
    
Then add checks in your host.cfg file. This is example of how to define one command check:

 *check_lenovo_ds2200.py -H 192.168.1.15 -u nagios -p 'p@ssw0rd' -P 22 -c sensors*

    define service {
    use                            generic-service
    hostgroup_name                 StorageServers
    service_description            Lenovo Sensors Health Check
    check_command                  check_lenovo_ds2200!nagios!p@ssw0rd!22!sensors
    check_interval                 10
    notifications_enabled          1
    }

Here is an example plugin answer for sensors:

      OK - All sensors are fine.
      CPU Temperature-Ctlr - Status: OK
      Capacitor Pack Temperature-Ctlr - Status: OK
      Expander Temperature-Ctlr - Status: OK
      Disk Controller Temperature-Ctlr - Status: OK
      Host IOC Temperature-Ctlr - Status: OK
      CPU Temperature-Ctlr - Status: OK
      Capacitor Pack Temperature-Ctlr - Status: OK
      Expander Temperature-Ctlr - Status: OK
      Disk Controller Temperature-Ctlr - Status: OK
      Host IOC Temperature-Ctlr - Status: OK
      Capacitor Pack Voltage-Ctlr - Status: OK
      Capacitor Cell 1 Voltage-Ctlr - Status: OK
      Capacitor Cell 2 Voltage-Ctlr - Status: OK
      Capacitor Cell 3 Voltage-Ctlr - Status: OK
      Capacitor Cell 4 Voltage-Ctlr - Status: OK
      Capacitor Pack Voltage-Ctlr - Status: OK
      Capacitor Cell 1 Voltage-Ctlr - Status: OK
      Capacitor Cell 2 Voltage-Ctlr - Status: OK
      Capacitor Cell 3 Voltage-Ctlr - Status: OK
      Capacitor Cell 4 Voltage-Ctlr - Status: OK
      Capacitor Charge-Ctlr - Status: OK
      Capacitor Charge-Ctlr - Status: OK
      Overall Unit - Status: OK
      Ops Panel Ambient - Status: OK
      Midplane - Status: OK
      SBB IOM Inlet Temperature Loc: - Status: OK
      Expander Internal Temperature Loc: lower-IOM - Status: OK
      SBB IOM Inlet Temperature Loc: - Status: OK
      Expander Internal Temperature Loc: upper-IOM - Status: OK
      Temperature Inlet Loc: - Status: OK
      Temperature Hotspot Loc: - Status: OK
      Temperature Inlet Loc: - Status: OK
      Temperature Hotspot Loc: - Status: OK
      Voltage 12V Rail Loc: - Status: OK
      Voltage 5V Rail Loc: - Status: OK
      Voltage 12V Rail Loc: - Status: OK
      Voltage 5V Rail Loc: - Status: OK
      Current 12V Rail Loc: - Status: OK
      Current 5V Rail Loc: - Status: OK
      Current 12V Rail Loc: - Status: OK
      Current 5V Rail Loc: - Status: OK

