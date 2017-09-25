import shelve
from shot import Shot
import os
from timecode import Timecode
from sys import argv
from xml.etree.ElementTree import parse
from pysrt import SubRipFile, SubRipItem, SubRipTime
import pprint
import xml.etree.ElementTree

# Creating a shelve to store all shots in a persitent file
# shotlist = shelve.open('shotlistest-shelve')

def add_shot_to_shotlist(shotcode, shot):
    '''
    Adds shot to the shotlist shelve
    :param shot:
    :param shotcode:
    :return:
    '''

    shotlist[shotcode] = shot

def print_shotlist():
    for key in shotlist:
        print(key, '=>\n ', shotlist[key], shotlist[key].shotCode, shotlist[key].tcIn)

if __name__ == '__main__':

    print(shotlist)
    print_shotlist()


    # CLose the shelve
    shotlist.close()


################ Ignore ... old ##########################

# shotlist.clear()


