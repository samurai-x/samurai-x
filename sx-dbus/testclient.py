import sys
from traceback import print_exc

import dbus

def main():
    bus = dbus.SessionBus()

    remote_object = bus.get_object("org.samuraix", "/dbus")
    iface = dbus.Interface(remote_object, "org.samuraix.DBusInterface")
    print iface.hello(sys.argv[1])



if __name__ == '__main__':
    main()

