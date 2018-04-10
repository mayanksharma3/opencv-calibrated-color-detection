import numpy as np
import cv2
import ast
import imutils

rect = (0, 0, 0, 0)
startPoint = False
endPoint = False
freezeFrame = False
lower = None
upper = None
frame = None
bounds_file = open("signatures.txt", "r")
previous = ast.literal_eval(bounds_file.readline())
bounds_file.close()


def on_mouse(event, x, y, flags, params):
	global rect, startPoint, endPoint, freezeFrame, lower, upper
	if event == cv2.EVENT_LBUTTONDOWN:
		if startPoint is True and endPoint is True:
			startPoint = False
			endPoint = False
			rect = (0, 0, 0, 0)
		if not startPoint:
			rect = (x, y, 0, 0)
			startPoint = True
			freezeFrame = True

	elif event == cv2.EVENT_MOUSEMOVE:
		if startPoint:
			cv2.rectangle(frame, (rect[0], rect[1]), (x, y), (255, 255, 255), 1)
			cv2.imshow('frame', frame)
	elif event == cv2.EVENT_LBUTTONUP:
		freezeFrame = False
		if not endPoint:
			rect = (rect[0], rect[1], x, y)
			roi = frame[rect[1]:rect[3], rect[0]: rect[2]]
			lower = [0, 0, 0]
			upper = [0, 0, 0]
			print "Processing..."
			for row in roi:
				for pix in row:
					if sum(lower) == 0:
						lower = pix
					lum_lower = (0.2126 * lower[2] + 0.7152 * lower[1] + 0.0722 * lower[0])
					lum_upper = 0.2126 * upper[2] + 0.7152 * upper[1] + 0.0722 * upper[0]
					lum_pix = (0.2126 * pix[2] + 0.7152 * pix[1] + 0.0722 * pix[0])
					if lum_pix < lum_lower:
						lower = pix - 10
					elif lum_pix > lum_upper:
						upper = pix + 10
			endPoint = True
			print "Bounds Found!"


def nothing(x):
	pass


def print_colors():
	color_info = ast.literal_eval(open("signatures.txt", "r").readline())
	for x in range(0, len(color_info)):
		if color_info[x] is not None:
			print "%s: %s" % (x, color_info[x]['color'])
		else:
			print "%s: Empty" % x


cap = cv2.VideoCapture(0)
print_colors()


def calibrate():
	cv2.namedWindow('frame')
	cv2.setMouseCallback('frame', on_mouse)
	cv2.createTrackbar('Signature', 'frame', 0, 10, nothing)
	global startPoint, endPoint, frame
	while True:
		(grabbed, frame) = cap.read()
		frame = imutils.resize(frame, width=600)
		frame_to_show = frame.copy()
		frame = cv2.medianBlur(frame, 15)
		if not freezeFrame:
			cv2.imshow('frame', frame_to_show)
		if startPoint is True and endPoint is True:
			pos = cv2.getTrackbarPos('Signature', 'frame')
			cv2.destroyAllWindows()
			startPoint = False
			endPoint = False
			if previous[pos] is not None:
				check = raw_input(
					"There already is a signature in this location. Are you sure you want to overwrite it? (Y/N) ")
				if check == "N":
					break
				elif check != "Y":
					print "Not a valid response. Will take it as No."
					break
			name = raw_input("What do you want to name that? ")
			shape = raw_input("What shape would you like to look for? ('circle' or 'rectangle') ")
			if shape != "circle" and shape != "rectangle":
				print "Not an option. Defaulting to rectangle"
				shape = "rectangle"
			previous[pos] = {"color": name, "bounds": [np.array_str(lower), np.array_str(upper)], "preferred_shape": shape}
			sig_file = open("signatures.txt", "w")
			sig_file.write(str(previous))
			sig_file.close()
			print_colors()
			print "Color saved! Change signature and calibrate another color or press Esc to exit."
			cv2.destroyAllWindows()
			calibrate()
		key = cv2.waitKey(1)
		if key == 27:
			exit()
	calibrate()


calibrate()
