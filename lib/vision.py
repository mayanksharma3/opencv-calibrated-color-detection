from math import pi

import numpy as np
import imutils
import cv2
import ast


class Vision(object):
	def __init__(self, signature_filepath, camera_index=0):
		self.sig_file = open("../" + signature_filepath, "r")
		self.camera = cv2.VideoCapture(camera_index)
		self.color_info = ast.literal_eval(self.sig_file.readline())
		self.colors = len(self.color_info)

	def get_color_info(self, show_feed=True, show_max=True, shape="rectangle"):
		(grabbed, frame) = self.camera.read()
		result = []
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		for x in range(0, self.colors):
			if not self.color_info[x]:
				continue
			lower = np.fromstring(self.color_info[x]['bounds'][0][1:-1], dtype=int, sep=' ')
			upper = np.fromstring(self.color_info[x]['bounds'][1][1:-1], dtype=int, sep=' ')
			mask = cv2.inRange(blurred, lower, upper)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)
			contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

			if len(contours) > 0:
				if show_max:
					contours = [max(contours, key=cv2.contourArea)]
				for c in contours:
					if shape == "rectangle":
						rect = cv2.minAreaRect(c)
						box = cv2.boxPoints(rect)
						box = np.int0(box)
						if cv2.contourArea(box) > 5000:
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
					elif shape == "circle":
						((ax, ay), radius) = cv2.minEnclosingCircle(c)
						M = cv2.moments(c)
						cx = int(M["m10"] / M["m00"])
						cy = int(M["m01"] / M["m00"])
						area = pi * radius ** 2
						if area > 5000:
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
