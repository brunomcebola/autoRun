import sys
import subprocess
import os
import time
import signal
import getopt
from multiprocessing import Process, Value

comp = ""
c_file = ""
version = '1.1.0'

def run(comp, file, pid, exit):
    try:
        subprocess.call([comp, "-std=c99", file+".c", "-o", file])
        cmd = './' + file;
        for x in range(3, len(sys.argv)):
            cmd += ' ' + sys.argv[x]
        os.system("clear")
        print("Program updated!!!\n")
        prog = os.system(cmd)
        pid.value = prog.pid
    except:
        print("\nSomething went wrong...\n")
        exit.value = True
        sys.exit()

def cmd_flags(argv):
    try:
        opts, args = getopt.getopt(argv,"hvc:",["help"])
        if(opts == []):
            print_option()
            sys.exit(2)
    except getopt.GetoptError:
        print_option()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_option()
            sys.exit(2)
        elif opt in ("-v"):
            print('\nVersion: {}\n'.format(version))
            sys.exit(2)
        elif opt == "-c":
            global comp, c_file
            c_file = arg
            comp = "gcc"


def print_option():
    print('\nUsage: auto_run.py [options] <input file(s)> <adicional parameters(s)>')
    print('\nOptions:')
    print('  -h, --help               Show program execution options')
    print('  -v                       Show program current version')
    print('  -c <source code> <args>  Compiles and runs C file')
    print('')

if __name__ == "__main__":

    cmd_flags(sys.argv[1:])

    pid = Value('i', 0)
    exit = Value('i', False)
    program = Process(target=run, args=(comp, c_file, pid, exit))
    program.start()

    dateOriginal = time.ctime(os.path.getmtime(c_file+".c"))

    while(True):
        dateModified = time.ctime(os.path.getmtime(c_file+".c"))
        if(dateOriginal != dateModified):
            dateOriginal = dateModified
            program.terminate()
            program = Process(target=run, args=(comp, c_file, pid, exit))
            program.start()
        if(exit.value):
            sys.exit()
