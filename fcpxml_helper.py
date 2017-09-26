
###########################################################################

def fcpx_timevalue_to_seconds(source, fps=24):
    """
    Function to convert between the fcpx timevalue (eg. 500/2400s = 5 frames, 3600s = 3600 seconds) to frames
    :param source:
    :param fps: Default is 24. We dont support drop frame standards yet.
    :return: seconds (this should be saver to do the timecode calculation later)
    """

    # TODO: Make it more generic also for durations like the fps
    # if the number contains a '/'
    if source.find('/') > 1:
        # print('yeah this is this damn format')
        numerator = source.split('/')[0]
        denominator = source.split('/')[1].split('s')[0]
        seconds = int(numerator) / int(denominator)
        frames = seconds * fps
        # print('Frames: ', frames)
        # print('Seconds: ', seconds)
        # print('Timecode: ', tc_from_frames(frames))
        return seconds

    # if not it's probably just seconds
    elif source.find('s'):
        # print("seems to be seconds only")
        seconds = int(source.split('s')[0])
        frames = seconds * fps
        # print('Seconds: ', seconds)
        # print('Timecode: ', tc_from_frames(frames))
        return seconds

###########################################################################

def tc_from_frames(frames, fps=24):
    """
    This is still kind of a cheat for representing time in timecode.
    Will replace later with real timecode object.
    Taken from here: https://github.com/ll-dev-team/thescripts/blob/master/python/m2s.py

    :param frames:
    :param fps: Default is 24. We don't support drop frame standards yet.
    :return: Timecode representation of a frame value
    """

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

