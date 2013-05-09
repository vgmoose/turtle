from socket import *
from thread import *
from sys import *
import struct,fcntl,termios, readline, os

PINK = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
my_name = 'User'

loop = True
clients = 2

if platform == 'win32':
    my_name = os.getenv('USERNAME')
else:
    my_name = os.getenv('USER')

def blank_current_readline():

    (rows,cols) = struct.unpack('hh', fcntl.ioctl(stdout, termios.TIOCGWINSZ,'1234'))

    text_len = len(PINK+my_name+': '+ENDC+readline.get_line_buffer())
    
    # ANSI escape sequences (All VT100 except ESC[0G)
    stdout.write('\x1b[2K')                         # Clear current line
    stdout.write('\x1b[1A\x1b[2K'*(text_len/cols))  # Move cursor up and clear line
    stdout.write('\x1b[0G')

def c_send(a):
    while(True):
        input = raw_input(PINK+my_name+': '+ENDC)
        if (input[0] == '/' and len(input)>1):
            exec_commands(input[1:], a)
        else:
            a.send(YELLOW+my_name+': '+ENDC+input)

def c_recv(a):
    while(True):
        string = a.recv(9999)
        if string:
            blank_current_readline()
            print string
            saveme = readline.get_line_buffer().split('\n')
#            if (saveme[-1]):
            stdout.write(PINK+my_name+': '+ENDC+saveme[-1])
            stdout.flush()

def exec_commands(command, a):
    if (command[0:4] == 'nick'):
        global my_name
        old_name = my_name
        my_name = command[5:]
        print GREEN+"you are now known as "+PINK+my_name+ENDC
        a.send(GREEN+old_name+' is now known as '+YELLOW+my_name)
    elif (command[0:5] == 'leave'):
        exit()
    elif (command[0:5] == 'clear'):
        os.system([ 'clear', 'cls' ][ os.name == 'nt' ])
    elif (command[0:4] == 'exec'):
        os.system(command[5:])
    else:
        print GREEN+'/'+command.split()[0]+' isn\'t a valid command.'

tup = [c_send, c_recv]

def communicate(partner):
    [start_new_thread(tup[x], (partner,)) for x in range(0,clients)]

def messy_argument_parser(default):
    if (len(argv)==1):
        argv.append('')
        argv.append(default)
    elif (len(argv) == 2):
        if (':' in argv[1]):
            split = argv[1].split(':')
            argv.append(split[1])
            argv[1] = split[0]
        else:
            if argv[1].isdigit():
                argv.append(argv[1])
                argv[0] = 'localhost'
            else:
                argv.append(default)

messy_argument_parser(55225)

try:
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((argv[1], int(argv[2])))
    value = s.recv(9999)
    s.send(my_name)
    filler = "s are"
    if (int(value) == 1):
        filler = " is"
    print GREEN+ value + " user"+filler+" chatting"+ENDC
    communicate(s);
    
except:
    server = socket(AF_INET, SOCK_STREAM)
    print YELLOW+"nobody's here yet..."+ENDC
    
    server.bind(('', int(argv[2])))
    server.listen(0)
    conn, addr = server.accept()
    conn.send(str(clients-1))
    print GREEN+conn.recv(9999)+" connected"+ENDC
    communicate(conn);

        
while(loop):
    pass