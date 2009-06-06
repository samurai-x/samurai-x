import sys
from traceback import print_exc

import dbus

def main():
    bus = dbus.SessionBus()

    remote_object = bus.get_object("org.samuraix.ControlService",
                                   "/ControlObject")
    iface = dbus.Interface(remote_object, "org.samuraix.ControlInterface")
    iface.action(sys.argv[1])



if __name__ == '__main__':
    main()

