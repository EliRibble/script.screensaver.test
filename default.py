import sys
import xbmcaddon
import xbmcgui
import xbmc
import logging
import serial

Addon = xbmcaddon.Addon('script.screensaver.rs232tvoff')

__scriptname__ = Addon.getAddonInfo('name')
__path__ = Addon.getAddonInfo('path')

LOGGER = logging.getLogger('rs232tvoff')

def telltv(connection, command):
    LOGGER.info('Sending to TV: %s', command)
    connection.write('{}\r'.format(command))
    response = ''
    while not response.endswith('x'):
        response += connection.read()
    return response
    
def createconnection():
    return serial.Serial('/dev/ttyUSB0', 9600, parity=serial.PARITY_NONE, stopbits=1, timeout=3)

class Screensaver(xbmcgui.WindowXMLDialog):
    class ExitMonitor(xbmc.Monitor):
        def __init__(self, exit_callback):
            self.exit_callback = exit_callback
            print("init called")

        def onScreensaverDeactivated(self):
            print '3 ExitMonitor: sending exit_callback'
            self.exit_callback()

    def onInit(self):
        print("Initializing screensaver")
        connection = createconnection()
        telltv(connection, 'ka 0 0')
        self.monitor = self.ExitMonitor(self.exit)

    def exit(self):
        print '4 Screensaver: Exit requested'
        connection = createconnection()
        telltv(connection, 'ka 0 1')
        self.close()

if __name__ == '__main__':
    print '1 Python Screensaver Started'
    screensaver_gui = Screensaver(
            'script-%s-main.xml' % __scriptname__,
            __path__,
            'default',
        )
    screensaver_gui.doModal()
    print '5 Python Screensaver Exited'
    del screensaver_gui
    sys.modules.clear()
