from cflib.drivers.crazyradio import Crazyradio

# cr = Crazyradio()


import usb
import sys
import time


def findDevice(vid, pid):
    busses = usb.busses()
    print "available busses : ", busses
    print "vid: ", vid
    for bus in busses:
        for device in bus.device`s:
            print device.idVendor, "vendor"
            if device.idVendor == vid:
                if device.idProduct == pid:
                    return device
    return None


def launchBootloader(verbose=False):
    dev = findDevice(0x1915, 0x7777)
    if dev == None:
        dev = findDevice(0x1915, 0x0101)
        if dev == None:
            if verbose:
                print "Error!, cannot find the CrazyRadio USB dongle!"
            return -1
        else:
            if verbose:
                print "Bootloader already launched."
            return 0

    handle = dev.open()

    if verbose:
        sys.stdout.write("Launch bootloader ")
        sys.stdout.flush()

    # Send the command to arm the bootloader
    handle.controlMsg(0x40, 0xFF, (), value=0, index=0, timeout=100)

    # resets to bootloader (Can fail as the device will disapear)
    try:
        handle.reset()
    except usb.USBError:
        pass

    # Wait for the bootloader to appear...
    dev = None

    for i in range(0, 4):
        if verbose:
            sys.stdout.write(".")
            sys.stdout.flush()
        time.sleep(0.5)
        dev = findDevice(0x1915, 0x0101)
        if dev != None:
            break

    if verbose:
        print ""

    if dev == None:
        if verbose:
            print "Error!, bootloader not started"
        return -2

    if verbose:
        print "Bootloader started"

    return 0


if __name__ == "__main__":
    sys.exit(launchBootloader(True))
