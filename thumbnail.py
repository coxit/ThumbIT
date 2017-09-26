import os
import subprocess

import cv2


class ThumbnailMaker:
    # TODO: Parralize the output process

    def __init__(self, source_movie, export_format='png', export_path='export/'):
        """

        :param source_movie:
        :param export_format:
        :param export_path:
        """
        self.source_movie = source_movie
        self.export_format = export_format
        self.export_path = export_path
        self.exported_frame_path = ''

        # Check if output path exists. If not create.
        if not os.path.exists(export_path):
            os.makedirs(export_path)

    ####################################################################################################

    def export_frame(self, frame_second, export_filename, overwrite=True):
        '''
        Does not resize the frame right away
        :param overwrite:
        :param frame_second: temporal position fo the frame we want to extract
        :param export_filename: How to name the file
        :return: path to generated file
        '''

        ffmpeg_flags = ''

        print('Exporting Frame at second {} from movie: {}'.format(frame_second, self.source_movie))

        # Check if we want to overwrite existing files
        if overwrite:
            ffmpeg_flags = '-y'
            print('(Will overwrite existing file)')

        # TODO: This is very fragile especially for the output path. Need to improve
        ffmpeg_command = 'ffmpeg {} -ss {} -i {} -vframes 1 {}{}.{}'.format(ffmpeg_flags,
                                                                            frame_second,
                                                                            self.source_movie,
                                                                            self.export_path,
                                                                            export_filename,
                                                                            self.export_format)

        print('Running ffmpeg with the following command:')
        print('{} \n'.format(ffmpeg_command))

        # Running FFMPEG
        # TODO: Hide the ffmpeg shell output or make it more readable.
        # Changed from call to run
        subprocess.run(ffmpeg_command, shell=True)

        # return path to output
        exported_frame_path = '{}{}.{}'.format(self.export_path, export_filename, self.export_format)

        print('\nExported frame to: {}'.format(exported_frame_path))

        self.exported_frame_path = exported_frame_path

        return exported_frame_path

    ####################################################################################################

    def export_thumbnail_constrained(self, target_width=600):
        '''
        Creates a thumbail for the frame created by the class
        Currently using the CV2 Library
        :param target_width: Widht in pixels
        :return: thumbnail_file
        '''

        # Read Image
        image = cv2.imread(self.exported_frame_path)

        # Calculate the Size of the thumbnail
        height, width = image.shape[:2]
        thumbnail_width = target_width
        thumbnail_height = int((target_width / width) * height)
        thumbnail_size = (thumbnail_width, thumbnail_height)  # This is x * y ... not sure why

        # Resize the image
        resized_image = cv2.resize(image, thumbnail_size, interpolation=cv2.INTER_AREA)

        # Define Filename
        thumbnail_filename = self.exported_frame_path
        thumbnail_filename = thumbnail_filename.split('.')[-2] + "_" + str(target_width) + "px." + \
                             thumbnail_filename.split('.')[-1]
        print("Created a thumbnail: {} \n".format(thumbnail_filename))

        # Write the new thumbnail
        cv2.imwrite(thumbnail_filename, resized_image)

        print('--------------------------------------------------------------')

        # Return thumbnail file
        return thumbnail_filename

    ####################################################################################################


    def export_frames(self, framelist, thumbnail=True):
        '''
        Not using the shotlist for now ... wanna keep this more generic
        :param framelist: list with the second the thumbnail should be taken from and the thumbnail filename
        :param thumbnail: function generates frames and thumbnails by default
        :return:
        '''

        i = 0

        for tn in framelist:

            # Export Frames
            b = self.export_frame(framelist[i][0], framelist[i][1])

            # If we also need a thumbnail
            if thumbnail:
                self.export_thumbnail_constrained()

            i = i + 1

        return framelist


if __name__ == '__main__':
    # Just for testing purposes
    print('Class test:')

    movieFile = 'tests/movie_2.mov'
    exportPath = 'export/'
    # sizes = [(120, 120), (720, 720), (1600, 1600)]
    framelist = {}

    t = ThumbnailMaker(movieFile, 'jpg')
    t.export_frames(shotlist)
    # t.export_frame(1, 'sam_xxxx')
    t.export_thumbnail_constrained()
    # t.export_thumbnail_from_image()
