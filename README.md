# OpenCV Calibrated Color Detection

Tracks multiple colors based on colors you calibrate beforehand

### Setup

1. Clone this repo: `git clone https://github.com/mayanksharma3/opencv-calibrated-color-detection.git`
2. Install OpenCV: `pip install opencv-python`

### Calibrating Colors

1. Run `python calibrate.py`. It should open a video-stream with a signatures bar on the top. 
2. Select which signature you wish to calibrate the color against using the top bar (0-9)
3. Hold the object/color in the frame and drag a square across an area where the main color is present
4. Type in the label for that color in the terminal
5. Repeat this for up to 10 colors, changing the signature location from the top bar every time

_Note: Signature information is stored in 'signatures.txt'_

### Tracking colors

Example code:

```python
from lib.vision import Vision
vision = Vision("signatures.txt")
while True:
	blocks = vision.get_color_info()
	if len(blocks) > 0:
		for block in blocks:
			print "Area: {}	X: {}	Y: {}	Color: {}".format(block['area'], block['x'], block['y'], block['color'])
	else:
		print "No major blocks in sight"
```

###  Vision Class

**Vision Init**

Arguments:
 - signature_filepath - (required) path to "signatures.txt"
 - camera_index - (optional, default: 0) index of camera to take feed from

**get_color_info()**

Arguments:
 - show_feed - (optional, default: True) toggle for showing graphical feed or not
 - show_max - (optional, default: True) toggle for showing the biggest area of a color, or to show all the shapes with the color present
 - shape - (optional, default: "rectangle") which shape the contour of the color should be. _"circle" or "rectangle"_

Return:
 - List of dicts of all the signatures seen in the frame
 
 
