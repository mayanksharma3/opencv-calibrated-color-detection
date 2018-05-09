from math import pi

import numpy as np
import cv2
import ast
from imutils.video import VideoStream
import imutils
from pylab import array, uint8


class Vision(object):
	def __init__(self, sig_file, camera_index=0):
		self.camera = VideoStream(0).start()
		self.color_info = ast.literal_eval(sig_file.readline())
		self.colors = len(self.color_info)

	def get_color_info(self, show_feed=True, show_max=True):
		frame = self.camera.read()
		frame = imutils.resize(frame, width=400)
		result = []
		image = frame
		max_intensity = 255.0  # depends on dtype of image data
		phi = 1
		theta = 1
		newImage1 = (max_intensity / phi) * (image / (max_intensity / theta)) ** 2
		newImage1 = array(newImage1, dtype=uint8)
		blurred = cv2.GaussianBlur(newImage1, (11, 11), 0)
		frame = newImage1

		for x in range(0, self.colors):
			if not self.color_info[x]:
				continue
			lower = np.fromstring(self.color_info[x]['bounds'][0][1:-1], dtype=int, sep=' ')
			upper = np.fromstring(self.color_info[x]['bounds'][1][1:-1], dtype=int, sep=' ')
			mask = cv2.inRange(blurred, lower, upper)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)
			contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			# cv2.imshow(self.color_info[x]['color'], mask)
			if len(contours) > 0:
				if show_max:
					contours = [max(contours, key=cv2.contourArea)]
				for c in contours:
					if self.color_info[x]['preferred_shape'] == "rectangle":
						rect = cv2.minAreaRect(c)
						box = cv2.boxPoints(rect)
						box = np.int0(box)
						if cv2.contourArea(box) > 3000:
							cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
							font = cv2.QT_FONT_NORMAL
							cv2.putText(frame, self.color_info[x]['color'], (box[1][0], box[1][1]), font, 0.5,
										(255, 255, 255), 1,
										cv2.LINE_AA)
							M = cv2.moments(box)
							cx = int(M['m10'] / M['m00'])
							cy = int(M['m01'] / M['m00'])
							result.append(
								{'area': cv2.contourArea(box), 'x': cx, 'y': cy, 'color': self.color_info[x]['color']})
					else:
						((ax, ay), radius) = cv2.minEnclosingCircle(c)
						M = cv2.moments(c)
						cx = int(M["m10"] / M["m00"])
						cy = int(M["m01"] / M["m00"])
						area = pi * radius ** 2
						if area > 3000:
							cv2.circle(frame, (int(ax), int(ay)), int(radius), (0, 0, 255), 2)
							font = cv2.QT_FONT_NORMAL
							cv2.putText(frame, self.color_info[x]['color'], (int(ax), int(ay)), font, 0.5,
										(255, 255, 255), 1,
										cv2.LINE_AA)
							result.append(
								{'area': radius, 'x': cx, 'y': cy, 'color': self.color_info[x]['color']})
		if show_feed:
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1)
			if key == 27:
				exit()
		return result
