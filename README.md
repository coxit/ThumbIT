# ThumbIT
Read FCPX-XML and Movie file to create thumbnails for each clip on the timeline.

### Disclaimer
This is a personal project to learn python and to solve some day to day tasks for vfx editorial.
Tested on MacOSX only.

### Usage

##### Final Cut Pro X

The script will search for text overlays for each clip to define the file naming. 
If no text overlay is found, it creates a generic file name.
- Export one timeline to FCPXML 1.6
- Export one quicktime movie

##### Command line interface:

` python thumbit.py myproject.fcpxml mymovie.mov `

Optional:

```
-dest [path for exported thumbnails]
-ext [file format for thumbnails (jpg, png)]
```

### Requires

- Python 3
- MMPEG
- CV2

### Planned Features
- Support for drop frame formats (eg 29,97fps)
- XLS import: Tumbnail, Shot Data.

### Limitations
- No support for FCPX exported from Adobe Premier
- No support for drop frame formats