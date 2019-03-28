# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# THe Python socket API is based closely on the Berkeley sockets API which
# was originally written for the C programming language.
#
# https://en.wikipedia.org/wiki/Berkeley_sockets
#
# The API is more flexible than you need, and it does some quirky things to
# provide that flexibility. I recommend tutorials instead of complete
# descriptions because those can skip the archaic bits. (The API was released
# more than 35 years ago!)
import socket
import time
# Read this many bytes at a time of a command. Each socket holds a buffer of
# data that comes in. If the buffer fills up before you can read it then TCP
# will slow down transmission so you can keep up. We expect that most commands
# will be shorter than this.
COMMAND_BUFFER_SIZE = 256
def CreateServerSocket(port):
    """Creates a socket that listens on a specified port.
    Args:
    port: int from 0 to 2^16. Low numbered ports have defined purposes. Almost
    all predefined ports represent insecure protocols that have died out.
    Returns:
    An socket that implements TCP/IP.
    """
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(2)
    return serverSocket

def ConnectClientToServer(server_sock):
    print("...Trying to Connect")
    return server_sock.accept()

def CreateClientSocket(server_addr, port):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((server_addr, port))
    #queue up to 10 requests
    return clientSocket

def ReadCommand(sock):
    data = sock.recv(COMMAND_BUFFER_SIZE)
    return data

def ParseCommand(command):
    args = command.strip().split(' ')
    command = None
    if args:
        command = args[0]
    arg1 = None
    if len(args) > 1:
        arg1 = args[1]
    remainder = None
    if len(args) > 2:
        remainder = ' '.join(args[2:])
    return command, arg1, remainder

class KeyValueStore(object):
    def __init__(self):
        #declare the dictionary
        self.keyValueDictionary = {}
        # self.keyList = [] 

    def GetValue(self, key, max_age_in_sec=None):
        if key in self.keyValueDictionary:
            myValue= self.keyValueDictionary[key]
            if max_age_in_sec :
                currAge = time.time() - myValue[1] 
                if max_age_in_sec >= currAge:
                    return myValue[0]
                else:
                    del self.keyValueDictionary[key]
            else:
                return myValue[0]
        return None
        """Gets a cached value or `None`.
        Values older than `max_age_in_sec` seconds are not returned.
        Args:
        =key: string. The name of the key to get.
        max_age_in_sec: float. Maximum time since the value was placed in the
        KeyValueStore. If not specified then values do not time out.
        Returns:
         None or the value.
        """
        # Check if we 've ever put something in the cache.
    def StoreValue(self, key, value):
        self.keyValueDictionary[key] = (value, time.time())
        return value
    def Keys(self):
        """Returns a list of all keys in the datastore."""
        return self.keyValueDictionary.keys()
