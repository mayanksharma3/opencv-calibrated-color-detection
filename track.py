from lib.vision import Vision

vision = Vision(open("signatures.txt", "r"))

while True:
	blocks = vision.get_color_info()
	if len(blocks) > 0:
		for block in blocks:
			print "Area: {}	X: {}	Y: {}	Color: {}".format(block['area'], block['x'], block['y'], block['color'])
	else:
		print "No major blocks in sight"
