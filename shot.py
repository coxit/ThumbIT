import fcpxml_helper as fcpx

class Shot:
    '''
    Class to manage shots extracted from FCPXML files
    '''

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    # Add additional attributes for thumbnail
        if self.offset:
            self.thumbnail_sec = fcpx.fcpx_timevalue_to_seconds(self.offset)
        else:
            self.thumbnail_sec = ''

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

        # TODO: Might be handy to add some functionality to the class itself.
        # ###########################################################################
        #
        # def tc_from_frames(frames, fps=24):
        #     '''
        #     This is still kind of a cheat for representing time in timecode.
        #     Will replace later with real timecode object.
        #     Taken from here: https://github.com/ll-dev-team/thescripts/blob/master/python/m2s.py
        #
        #     :param frames:
        #     :param fps: Default is 24. We dont support drop frame standards yet.
        #     :return: Timecode representation of a frame value
        #     '''
        #
        #     the_frames = int(frames) % fps
        #     seconds = (frames - the_frames) / fps
        #     the_seconds = int(seconds % 60)
        #     minutes = (seconds - the_seconds) / 60
        #     the_minutes = int(minutes % 60)
        #     hours = (minutes - the_minutes) / 60
        #     str_hours = "{0:0>2}".format(int(hours))
        #     str_minutes = "{0:0>2}".format(int(the_minutes))
        #     str_seconds = "{0:0>2}".format(int(the_seconds))
        #     str_frames = "{0:0>2}".format(int(the_frames))
        #     str_filename_tc = '{}:{}:{}:{}'.format(str_hours, str_minutes, str_seconds, str_frames)
        #     return str_filename_tc
        #
        # def fcpx_timevalue_to_seconds(source, fps=24):
        #     '''
        #     Function to convert between the fcpx timevalue (eg. 500/2400s = 5 frames, 3600s = 3600 seconds) to frames
        #     :param source:
        #     :param fps: Default is 24. We dont support drop frame standards yet.
        #     :return: seconds (this should be saver to do the timecode calculation later)
        #     '''
        #     # if the number contains a '/'
        #     if source.find('/') > 1:
        #         print('yeah this is this damn format')
        #         numerator = source.split('/')[0]
        #         denominator = source.split('/')[1].split('s')[0]
        #         seconds = int(numerator) / int(denominator)
        #         frames = seconds * fps
        #         print('Frames: ', frames)
        #         print('Seconds: ', seconds)
        #         print('Timecode: ', tc_from_frames(frames))
        #         return seconds
        #
        #     # if not it's probably just seconds
        #     elif source.find('s'):
        #         print("seems to be seconds only")
        #         seconds = int(source.split('s')[0])
        #         frames = seconds * fps
        #         print('Seconds: ', seconds)
        #         print('Timecode: ', tc_from_frames(frames))
        #         return seconds


if __name__ == '__main__':
    timeline_format = {'frameDuration': '100/2400s', 'height': '1080', 'id': 'r1', 'name': 'FFVideoFormat1080p24',
                       'width': '1920', 'tcStart': '3600s', 'tcFormat': 'NDF', 'duration': '9200/2400s',
                       'audioLayout': 'stereo', 'audioRate': '48k', 'fps': 24}

    print("timeline format: ", timeline_format)

    # Knowhow:
    # The timecode display format, either drop frame (DF) or nondrop frame (NDF, the default).
    print('--------------------------------------------------------------')

    o = Shot({'name': 'auf_sam_0000_edit', 'offset': '3601s', 'ref': 'r2', 'duration': '1s',
              'start': '1s', 'audioRole': 'dialogue', 'tcFormat': 'NDF', 'shotCode': 'sam_0010a'})
    print(o.start)
    print('--------------------------------------------------------------')

    # o.__setattr__("thumbnail", "THUMBNAIL")
    # print(o.start)
    # print(o)

    print('--------------------------------------------------------------')

    # Calculate Sequence FPS
    sequence_fps = timeline_format['frameDuration']
