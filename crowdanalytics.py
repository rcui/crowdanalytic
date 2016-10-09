import sys
import getopt
import os

import socksy.py
import crowdcropper.py

def main(argv):
    try:
        args = getopt.getopt(argv, 'hi:', ['image='])
    except getopt.GetoptError:
        print 'crowdanalytics.py -i <image>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'crowdanalytics.py -i <image>'
            sys.exit()
        elif opt in ('-i', '--image'):
            image = arg


def init():
    fpath = os.getcwd()
    for img in os.listdir(os.path.join(fpath, 'dumpimg')):
        os.remove(img)
    


if __name__ == "__main__":
    main(sys.argv[1:])
