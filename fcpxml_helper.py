# From Apple Developer Docs:
# https://developer.apple.com/library/content/documentation/FinalCutProX/Reference/FinalCutProXXMLFormat/StoryElements/StoryElements.html#//apple_ref/doc/uid/TP40011227-CH13-SW14

# The time range for contained items is limited by their parent. The time range for anchored items is not
# limited by their parent; however, anchored items may be limited by an ancestor that either directly or
# indirectly contains the parent.

# Time values are expressed as a rational number of seconds with a 64-bit numerator and a 32-bit denominator.

# Frame rates for NTSC-compatible media, for example, use a frame duration of 1001/30000s (29.97 fps) or
# 1001/60000s (59.94 fps). If a time value is equal to a whole number of seconds, the fraction may be reduced
# into whole seconds (for example, 5s).

# Timing attribute values are expected to be a multiple of the frame duration for the respective timeline. Otherwise,
# Final Cut Pro X has to insert a gap to maintain the specified timing upon import. A warning message appears when this happens.
#

# FCPX Supported Video Formats
# https://developer.apple.com/library/content/documentation/FinalCutProX/Reference/FinalCutProXXMLFormat/FCPXMLSupportedIdentifiers/FCPXMLSupportedIdentifiers.html#//apple_ref/doc/uid/TP40011227-CH3-SW1


###########################################################################

def tc_from_frames(frames, fps=24):
    """
    This is still kind of a cheat for representing time in timecode.
    Taken from here: https://github.com/ll-dev-team/thescripts/blob/master/python/m2s.py

    :rtype: String
    :param frames:
    :param fps: Default is 24. We don't support drop frame standards yet.
    :return: Timecode representation of a frame value
    """
    # TODO: Handle TimeCode
    the_frames = int(frames) % fps
    seconds = (frames - the_frames) / fps
    the_seconds = int(seconds % 60)
    minutes = (seconds - the_seconds) / 60
    the_minutes = int(minutes % 60)
    hours = (minutes - the_minutes) / 60
    str_hours = "{0:0>2}".format(int(hours))
    str_minutes = "{0:0>2}".format(int(the_minutes))
    str_seconds = "{0:0>2}".format(int(the_seconds))
    str_frames = "{0:0>2}".format(int(the_frames))
    str_filename_tc = '{}:{}:{}:{}'.format(str_hours, str_minutes, str_seconds, str_frames)
    return str_filename_tc


###########################################################################

def seconds_from_timevalue(source, fps=24):
    """
    Function to convert between the fcpx timevalue (eg. 500/2400s = 5 frames, 3600s = 3600 seconds) to frames
    :param source:
    :param fps: default is 24 fps. Does not support drop frame standards yet.
    :return: timevalue (length, duration, offset, start) in seconds
    """

    # if the number contains a '/'
    if source.find('/') > 1:
        numerator = source.split('/')[0]
        denominator = source.split('/')[1].split('s')[0]
        seconds = int(numerator) / int(denominator)
        # frames = seconds * fps
        # print('Frames: ', frames)
        # print('Seconds: ', seconds)
        # print('Timecode: ', tc_from_frames(frames))
        return seconds

    # if not it's probably just seconds
    elif source.find('s'):
        seconds = int(source.split('s')[0])
        # frames = seconds * fps
        # print('Seconds: ', seconds)
        # print('Timecode: ', tc_from_frames(frames))
        return seconds


def fps_from_timeline_format(arg):
    # TODO: New Function: Fps from format/name in XML to support more standards

    arg = arg.strip('_16x9')
    arg = arg.strip("FFVideoFormat")

    if 'i' in arg:
        arg = arg.rsplit('i')[1]
    elif 'p' in arg:
        arg = arg.rsplit('p')[1]

    if len(arg) > 2:
        fps = int(arg) / 100
    else:
        fps = arg


    return fps


if __name__ == '__main__':

    # Testing scenarios for timevalue
    # Todo: Write better test that compares to correct values.
    testcases_timevalue = [['500/2400s', '0.20s', '5 frames', '00:00:00:05'],
                           ['3600s', '3603s', 'x', '01:00:02:00'],
                           ['8648700/2400s', 'x', 'x', '00:00:00:00'],
                           ['8700/2400s', 'x', 'x', '00:00:00:00'],
                           ['1500/2400s', 'x', 'x', '00:00:00:00'],
                           ['1s', 'x', 'x', '00:00:00:00'],
                           ['9200/2400s', 'x', 'x', '00:00:00:00']
                           ]
    print('\nTesting scenarios for timevalue')
    for x in testcases_timevalue:
        print('Value: {} => {} seconds or {} (@24fps)'.format(x[0],
                                                              seconds_from_timevalue(x[0]),
                                                              tc_from_frames(24 * seconds_from_timevalue(x[0])
                                                                             )))
    print('\nTesting scenarios for format')
    testcases_formats = [
        ['FFVideoFormatRateUndefined', '24.0'],
        ['FFVideoFormat1080i50', '50.0'],
        ['FFVideoFormat1080i5994', '59.94'],
        ['FFVideoFormat1080p2398', '23.98'],
        ['FFVideoFormat1080p24', '24.0'],
        ['FFVideoFormat1080p25', '25.0'],
        ['FFVideoFormat720p24', '24.0'],
        ['FFVideoFormatDV720x480i5994', '59.94'],
        ['FFVideoFormatDV720x480i5994_16x9', '59.94']
    ]

    for x in testcases_formats:
        print('Value: {} => {} correct: {}'.format(x[0], fps_from_timeline_format(x[0]), x[1]))

