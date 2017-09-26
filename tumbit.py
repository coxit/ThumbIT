import argparse
import os
import shelve
import xml.etree.ElementTree
from datetime import datetime

import fcpxml_helper as fcpx
import shotlist
from shot import Shot
from thumbnail import ThumbnailMaker

'''

ToDo First Versions:
[x] Add Thumbnail position to shotlist [Done]
[x] Ass CLI argument for input movie
[x] Set output path
[x] Create FFmpeg module to generate thumbnail
[x] Export Thumbnails
[-] Export Excel list
    - support custom ordering of collomns

ToDo Features:
- support drop frame timecodes
- support markers
    - Add markers to a shot
    - Collect markers in extra list

'''

print('-------------------------------------------------------------------')
print('THUMB IT v0.1 \n')

# combines resource and timeline attributes into one dict
srcTimelineFormat = {}
# export_format='png'
# export_path='export/'
# fcpxmlFile = ''
# movieFile =''
# exportPath = ''
# exportFormat = ''



###########################################################################
# Check if temp folder exist; if not create one.

# temp_dir = './tmp/' + str(datetime.today())+"/"
temp_dir = './tmp/'


def mkdir_p(filename):
    try:
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return True
    except:
        return False


if mkdir_p(temp_dir):
    print("Created temp dir: %s" % (os.path.dirname(temp_dir)))

###########################################################################
# Creat shotlist shelve


shotlist = shelve.open(temp_dir + "shotlist_shelve")


###########################################################################
# Main Function to read the fcpxml
def process_clips_in_fcpxml(fcpxml, movie, exportpath='export', exportformat='png'):
    '''
    Read an FCPXml file, create a shot list, export thumbnails
    :param exportformat:
    :param fcpxml: A valid Final Cut Pro X XML file
    :param movie: A quicktime movie (or anything else FFMPEG accepts
    :param exportpath: Destination for all exports
    :return:
    '''

    # Takes the path to the XML file and starts parsing
    tree = xml.etree.ElementTree.parse(fcpxml)
    root = tree.getroot()

    # Check if the file is a FCP XML
    check_xml_file(tree)

    # Get the format of the Timeline
    get_timeline_format(tree)

    # Extract Shots
    get_shots_from_fcpxml(tree)

    # Show the list we created
    # print_shotlist()

    # Create Frame Graps and Thumbnails
    create_thumbnails_from_shotlist(shotlist, movieFile, export_format=exportformat, export_path=exportpath)

    print("Done.")


###########################################################################
def create_thumbnails_from_shotlist(shotlist, movie, export_format='png', export_path='export/'):
    t = ThumbnailMaker(movieFile, export_format=export_format, export_path=export_path)

    framelist = []  # List of frames to be passed to Thumbmaker
    i = 1

    print('--------------------------------------------------------------')
    for key in shotlist:
        # print("Creating Thumbs: ", key, '=>', 'Thumbnail:', shotlist[key].thumbnail_sec, shotlist[key].shotCode)

        # FFMPEG counts seconds from the start of the timeline so we need to deduct start from offset
        timeline_start = fcpx.fcpx_timevalue_to_seconds(srcTimelineFormat['tcStart'])
        thumbnail_sec = shotlist[key].thumbnail_sec - timeline_start

        # add the thumbnail to the list
        templist = thumbnail_sec, shotlist[key].shotCode
        framelist.append(templist)


        # t.export_frame(1, 'sam_xxxx')
        # t.export_thumbnail_constrained()

    print('--------------------------------------------------------------')
    # print(framelist)

    # Call function to create frames and thumbnails
    result = t.export_frames(framelist, thumbnail=True)

    # print(result)
    return result


###########################################################################
def add_shot_to_shotlist(shotcode, shot):
    '''
    Adds shot to the shotlist shelve
    :param shot:
    :param shotcode:
    :return:
    '''

    shotlist[shotcode] = shot


###########################################################################
def print_shotlist():
    print('--------------------------------------------------------------')
    for key in shotlist:
        print(key, '=>\n ', shotlist[key])
    print('--------------------------------------------------------------')


###########################################################################
def get_timeline_format(tree):
    '''
    Get all important timeline settings
    :return: Dict with all values
    '''
    root = tree.getroot()

    # Store results in global var for now
    global srcTimelineFormat

    # FCP Resources Format
    found_format = root.findall('.//format')

    for element in found_format:
        # Print all attributes of the found element
        print('Reading timeline format ...')
        # pprint.pprint(element.attrib)

        # Add values to global srcTimelineFormat
        srcTimelineFormat['frameDuration'] = element.get('frameDuration')
        srcTimelineFormat['height'] = element.get('height')
        srcTimelineFormat['id'] = element.get('id')
        srcTimelineFormat['name'] = element.get('name')
        srcTimelineFormat['width'] = element.get('width')

    # FCP Sequence Attributes
    found_sequence = root.findall('.//sequence')

    for element in found_sequence:
        # Print all attributes of the found element
        print('Reading sequence format ...')
        # pprint.pprint(element.attrib)

        # Add values to global srcTimelineFormat
        srcTimelineFormat['tcStart'] = element.get('tcStart')
        srcTimelineFormat['tcFormat'] = element.get('tcFormat')
        srcTimelineFormat['duration'] = element.get('duration')
        srcTimelineFormat['audioLayout'] = element.get('audioLayout')
        srcTimelineFormat['audioRate'] = element.get('audioRate')

    # Add fps (frames per second) based on the Frame Durations value.
    print('\nProject format:')
    srcTimelineFormat['fps'] = int(srcTimelineFormat['frameDuration'].split('/')[1].strip('00s'))

    print(srcTimelineFormat)
    print('\n--------------------------------------------------------------')

    # Returns all values in one dict
    return srcTimelineFormat


###########################################################################
def get_shots_from_fcpxml(tree):
    '''
    Extracts shots from XML file
    :param tree:
    :return:
    '''
    root = tree.getroot()

    # davinci exports as clip, final cut pro as asset-clip
    all_clips = tree.findall('.//clip') + tree.findall('.//asset-clip')
    x = len(all_clips)
    i = 0

    print("Extracting Shots and adding them to the shotlist:")

    while x > i:
        clip = all_clips[i].attrib

        # TODO: What if we dont have text overlay? Still need a shotCode! Check if it works.
        # Add the shotcode based on the text clip we find in the timeline
        if all_clips[i].find('.//text-style') is not None:
            title = all_clips[i].find('.//text-style')
            clip['shotCode'] = title.text
        # If there is not text overlay we simply add a generic shot code
        else:
            clip['shotCode'] = "Shot_" + str(i)

        # Creat shot Object
        shot = Shot(clip)

        # Add the shot to the shotlist shelve
        add_shot_to_shotlist(clip['shotCode'], shot)
        print(title.text, '=', clip)

        i = i + 1


###########################################################################
# Function to check the XML File
def check_xml_file(tree):
    print("-------------- Let's get started -----------------------------")
    root = tree.getroot()
    print("Checking if it is a FCP XML File:")
    if root.tag == 'fcpxml':
        print("Oh yes ... it should be fine: ", root.tag, root.attrib)
        print('\n--------------------------------------------------------------')
        return
    else:
        print("Sorry dude, this seems to be the wrong file", root.tag, root.attrib, "\n")
        exit()


###########################################################################
# When Script is opened directly

if __name__ == '__main__':

    ###########################################################################
    # Command Line Interface


    parser = argparse.ArgumentParser(description='Extracting Thumbnails made easy',
                                     usage='%(prog)s xmlfile movie',
                                     epilog="Pretty easy, huh!?")
    parser.add_argument('xmlfile', metavar='xmlfile', type=str, nargs='+',
                        help='The XML file you wanna use')
    parser.add_argument('movieFile', metavar='movieFile', type=str, nargs='+',
                        help='The Movie file you wanna use')
    parser.add_argument('-dest', metavar='dest', type=str, nargs='+',
                        help='where you want to save the output')
    parser.add_argument('-ext', metavar='export_format', type=str, nargs='+',
                        help='Image Format of Thumbnails')
    args = parser.parse_args()

    ###########################################################################
    # These are the file we want to parse ...
    global fcpxmlFile, movieFile, exportPath, exportFormat
    fcpxmlFile = args.xmlfile[0]
    movieFile = args.movieFile[0]

    # Welcome the user and get started
    print('Well, well ... We are gonna work with this FCPXML file: ', fcpxmlFile)
    print('And this movie file: ', movieFile)

    # Assign arguments to local vars
    if args.dest is not None:
        exportPath = args.dest[0]
        if not exportPath.endswith('/'):
            exportPath = exportPath + "/"
        print('We will try to save the output here: ', exportPath)
    else:
        exportPath = 'export/'.format(str(datetime.today()))
        print('We will try to save the output here: ', exportPath)
    if args.ext is not None:
        exportFormat = args.ext[0]
        print('We will use {} as the image format for thumbnails.'.format(str(exportFormat).upper()))
    else:
        exportFormat = 'png'
        print('We will use {} as the image format for thumbnails.'.format(str(exportFormat).upper()))

    print('\n')
    # Call our main function
    process_clips_in_fcpxml(fcpxmlFile, movieFile, exportPath, exportFormat)
