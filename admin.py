#!/usr/bin/env python
import curses
import curses.textpad, curses.panel
import os, datetime, signal, sys

import os

def sigHandle(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, sigHandle)

def displayIP(addr):
    if addr == "DOWN":
        return "  "+addr
    return "IP "+str(addr)

def displayGW(addr):
    if addr is not "DOWN":
        return "GW "+str(addr)
    return ""

def displayNS(addr):
    if addr is not "DOWN":
        return "DNS "+str(addr)
    return ""
def staticIP(ipStack):
    intf = file("/etc/network/interfaces",'rw')
    lines = intf.readlines()
    lines.append("iface eth0 inet static")
    lines.append("address " +ipStack[0])
    lines.append("netmask " +ipStack[1])
    lines.append("gateway " +ipStack[2])
        

def main(win):
    optionSel=0
    pos=0
    dirty = False
    zeroL=True
    fourL = True
    fiveL=True
    while 1:
        curses.curs_set(0)
        stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.init_pair(1,curses.COLOR_RED,curses.COLOR_WHITE)
        stdscr.clear()

        sh,sw = stdscr.getmaxyx()

        if curses.is_term_resized(sh,sw):
            sh,sw = stdscr.getmaxyx()
            stdscr.clear()
            curses.resizeterm(sh,sw)
            stdscr.refresh()

        rows = sh/8.
        cols = sw/4.
        x = 0
        hPanel = stdscr.subwin(2,int(sw),x,0)
        x+=2
        topMid = stdscr.subwin(int(rows*2),int(sw),x,0)
        x+=int(rows*2)
        bottomMid = stdscr.subwin(int(rows*2),int(sw),x,0)
        x+=int(rows*2)
        leftFooter= stdscr.subwin(int(rows*2),30,x,0)
        rightFooter= stdscr.subwin(int(rows*2),int(sw)-30,x,29)


        topMid.border(1,1,0,1,1,1,1,1)
        bottomMid.border(1,1,0,1,1,1,1,1)

        leftFooter.border(1,0,0,1,1,0,1,1)
        rightFooter.border(0,1,0,1,0,1,1,1)


        dt = datetime.datetime.now()
        hPanel.addstr(0,0,dt.strftime("%m/%d/%y %H:%m"))
        hPanel.addstr(0,sw/2,"Sys Interface")
        hPanel.addstr(1,sw/2," Version 1.0")
        upTime = os.popen("uptime -p").read()

        if len(upTime) > 15:
            hPanel.addstr(0,sw-30,upTime)
        else:
            hPanel.addstr(0,sw-15,upTime)

        topMid.addstr(1,sw/2,"VPN Status",curses.A_BOLD)
        #need to run checks...see if tun is connected state
        topMid.addstr(2,(sw/2)-1, "Not Connected")

        bottomMid.addstr(1,sw/2,"Interfaces",curses.A_BOLD)

        interfaces = os.popen("nmcli d").read().split('\n')[1::]
        i1 = interfaces[0].split()
        i2 = interfaces[1].split()
        i3 = interfaces[2].split()

        ipcmd = "ip addr show "
        ipaddr1=[ i for i in os.popen(ipcmd+i1[0]).read().split("\n") if "inet" in i]
        ipaddr1=ipaddr1[0].strip().split(' ')[1] if len(ipaddr1)>0 else "DOWN"
        ipaddr2=[ i for i in os.popen(ipcmd+i2[0]).read().split("\n") if "inet" in i]
        ipaddr2=ipaddr2[0].strip().split(' ')[1] if len(ipaddr2)>0 else "DOWN"
        ipaddr3=[ i for i in os.popen(ipcmd+i3[0]).read().split("\n") if "inet" in i]
        ipaddr3=ipaddr3[0].strip().split(' ')[1] if len(ipaddr3)>0 else "DOWN"

        gwcmd = os.popen("netstat -r").read().split('\n')[2::]
        ifgw1=[ i.split(' ') for i in gwcmd if i1[0] in i][0]
        ifgw2=[ i.split(' ') for i in gwcmd if i2[0] in i][0]
        ifgw3=[ i.split(' ') for i in gwcmd if i3[0] in i][0]
        ifgw1 = [ i for i in ifgw1 if len(i) >=1 ][1]
        ifgw2 = [ i for i in ifgw2 if len(i) >=1 ][1]
        ifgw3 =  [ i for i in ifgw3 if len(i) >=1 ][1]


        bottomMid.addstr(2,3,i1[0])
        bottomMid.addstr(3,1,displayIP(ipaddr1))
        bottomMid.addstr(4,1,displayGW(ifgw1))
        bottomMid.addstr(5,1,displayNS(ipaddr1))

        bottomMid.addstr(2,(sw/2)+5,i2[0])
        bottomMid.addstr(3,sw/2,displayIP(ipaddr2))
        bottomMid.addstr(4,sw/2,displayGW(ifgw2))
        bottomMid.addstr(5,sw/2,displayNS(ipaddr2))

        bottomMid.addstr(2,(sw-20)+2,i3[0])
        bottomMid.addstr(3,sw-20,displayIP(ipaddr3))
        bottomMid.addstr(4,sw-20,displayGW(ifgw3))
        bottomMid.addstr(5,sw-20,displayNS(ipaddr3))


        hl = curses.color_pair(1)
        norm = curses.A_NORMAL

        leftFooter.addstr(1,10,"Admin Options")

        if pos == 0:
            leftFooter.addstr(2,1,"Set IP Address",hl)
        else:
            leftFooter.addstr(2,1,"Set IP Address",norm)

        if pos == 1:
            leftFooter.addstr(3,1,"Set DNS",hl)
        else:
            leftFooter.addstr(3,1,"Set DNS",norm)

        if pos == 2:
            leftFooter.addstr(4,1,"Ping",hl)
        else:
            leftFooter.addstr(4,1,"Ping",norm)

        if pos == 3:
            leftFooter.addstr(5,1,"Login",hl)
        else:
            leftFooter.addstr(5,1,"Login",norm)

        if pos == 4:
            leftFooter.addstr(6,1,"Reboot",hl)
        else:
            leftFooter.addstr(6,1,"Reboot",norm)
            
        if pos == 5:
            leftFooter.addstr(7,1,"Shutdown",hl)
        else:
            leftFooter.addstr(7,1,"Shutdown",norm)

        rightFooter.addstr(1,(sw/2)-30,"Input area")
        if dirty:
            if pos == 0 and zeroL:
                rightFooter.addstr(5,(sw/2)-30,"DHCP",hl)
                rightFooter.addstr(5,(sw/2)-10,"Static",norm)
            elif pos == 0 and not zeroL:
                rightFooter.addstr(5,(sw/2)-30,"DHCP",norm)
                rightFooter.addstr(5,(sw/2)-10,"Static",hl)
            if pos == 4 and fourL:
                rightFooter.addstr(5,(sw/2)-30,"Reboot",hl)
                rightFooter.addstr(5,(sw/2)-10,"Abort",norm)
            elif pos == 4 and not fourL:
                rightFooter.addstr(5,(sw/2)-30,"Reboot",norm)
                rightFooter.addstr(5,(sw/2)-10,"Abort",hl)
            if pos == 5 and fiveL:
                rightFooter.addstr(5,(sw/2)-30,"ShutDown",hl)
                rightFooter.addstr(5,(sw/2)-10,"Abort",norm)
            elif pos == 5 and not fiveL:
                rightFooter.addstr(5,(sw/2)-30,"ShutDown",norm)
                rightFooter.addstr(5,(sw/2)-10,"Abort",hl)


        hPanel.refresh()
        topMid.refresh()
        bottomMid.refresh()
        leftFooter.refresh()
        rightFooter.refresh()
        stdscr.refresh()

        optionSel=stdscr.getch()

        def curSel():
            output=""
            if pos == 0:
                if zeroL:
                    output= os.popen("dhclient-script BOUND").read()
                    dirty=False
                else:
                    curses.textpad.Textbox(stdscr).edit()
                    staticIP(txtReturn)
            elif pos == 1:
                curses.textpad.Textbox(stdscr).edit()
            elif pos == 2:
                curses.textpad.Textbox(stdscr).edit()
                
            elif pos == 3:
                    pass
            elif pos == 4:
                if fourL:
                    os.popen("shutdown -r")
                else:
                    dirty=False
            elif pos == 5:
                if fiveL:
                    os.popen("shutdown -h")
                else:
                    dirty=False
            else:
                output="Input area"
                rightFooter.addstr(1,sw/2,output[0])

        if optionSel == 258 and not dirty:
            if pos<5:
                pos+=1
        elif optionSel == 259 and not dirty:
            if pos>0: 
                pos-=1
        elif optionSel == ord('\n') and not dirty:
            dirty=True
            curses.flash()
        elif optionSel == ord('\n') and dirty:
            curSel()
            dirty=False
        elif optionSel == ord('q') and dirty:
            optionSelected = False
            dirty=False


        if optionSel == 260 and dirty:
            if pos == 0:
                zeroL=True
                rightFooter.addstr(5,(sw/2)-30,"DHCP",hl)
                rightFooter.addstr(5,(sw/2)-10,"Static",norm)
            elif pos == 4:
                fourL = True
                rightFooter.addstr(5,(sw/2)-30,"Reboot",hl)
                rightFooter.addstr(5,(sw/2)-10,"Abort",norm)
            elif pos == 5:
                fiveL = True
                rightFooter.addstr(5,(sw/2)-30,"ShutDown",hl)
                rightFooter.addstr(5,(sw/2)-10,"Abort",norm)

        if optionSel == 261 and dirty:
            if pos == 0:
                zeroL=False
                rightFooter.addstr(5,(sw/2)-30,"DHCP",norm)
                rightFooter.addstr(5,(sw/2)-10,"Static",hl)
            elif pos == 4:
                fourL = False
                rightFooter.addstr(5,(sw/2)-30,"Reboot",norm)
                rightFooter.addstr(5,(sw/2)-10,"Abort",hl)
            elif pos == 5 :
                fiveL = False
                rightFooter.addstr(5,(sw/2)-30,"ShutDown",norm)
                rightFooter.addstr(5,(sw/2)-10,"Abort",hl)

        hPanel.refresh()
        topMid.refresh()
        bottomMid.refresh()
        leftFooter.refresh()
        rightFooter.refresh()

        stdscr.refresh()


curses.wrapper(main)
