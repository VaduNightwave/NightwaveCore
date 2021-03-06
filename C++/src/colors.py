# -*- encoding: utf8 -*-

#
# GooCore - colors.py
# ©2018 Gooborg Studios: Vinyl Darkscratch, Light Apacha.
# http://www.gooborg.com/
#

import math

# RGB<>HSL color conversion
def RGB2HSL(r, g, b):
	# XXX Convert to fully utilizing 0-255 and 0-360 ranges for accuracy
	r = r / 255.0
	g = g / 255.0
	b = b / 255.0

	max_val = max(r, g, b)
	min_val = min(r, g, b)
	hue = saturation = luminosity = (max_val + min_val) / 2

	if max_val == min_val: hue = s = 0
	else:
		diff = max_val - min_val
		if luminosity > 0.5:
			if (2 - max_val - min_val) == 0: saturation = 0
			else: saturation = diff / (2 - max_val - min_val)
		else: saturation = diff / (max_val + min_val)

		if max_val == r:
			hue = (g - b) / diff
			if g < b: hue += 6.0
		elif max_val == g: hue = (b - r) / diff + 2.0
		elif max_val == b: hue = (r - g) / diff + 4.0

	hue = hue * 60
	saturation = saturation * 255
	luminosity = luminosity * 255

	return [int(hue), int(saturation), int(luminosity)]

def Hue2RGB(cc_p, cc_q, cc_t):
	# XXX Convert to fully utilizing 0-255 and 0-360 ranges for accuracy
	if (cc_t < 0.0): cc_t += 1
	if (cc_t > 1.0): cc_t -= 1
	if (cc_t < 1 / 6.0): return cc_p + (cc_q - cc_p) * 6.0 * cc_t
	if (cc_t < 1 / 2.0): return cc_q
	if (cc_t < 2 / 3.0): return cc_p + (cc_q - cc_p) * (2 / 3.0 - cc_t) * 6.0
	return cc_p

def HSL2RGB(hue, saturation, luminosity):
	# XXX Convert to fully utilizing 0-255 and 0-360 ranges for accuracy
	hue = hue / 360.0
	saturation = saturation / 255.0
	luminosity = luminosity / 255.0

	if (saturation == 0.0): red = green = blue = luminosity
	else:
		if luminosity < 0.5: q = luminosity * (1.0 + saturation)
		else: q = luminosity + saturation - luminosity * saturation
		p = 2.0 * luminosity - q

		red = Hue2RGB(p, q, hue + 1.0/3.0) * 255.0
		green = Hue2RGB(p, q, hue) * 255.0
		blue = Hue2RGB(p, q, hue - 1.0/3.0) * 255.0

	return [int(red), int(green), int(blue)]

# RGB<>HSV color conversion
def RGB2HSV(red, green, blue):
	max_val = max(red, green, blue)
	min_val = min(red, green, blue)
	diff = max_val - min_val
	velocity = max_val
	if max_val == 0: saturation = 0
	else: saturation = diff / max_val * 255

	if max_val == min_val:
		hue = 0
	else:
		if max_val == red:
			hue = (green - blue) * 60 / diff
			if green < blue: hue += 360
		elif max_val == green: hue = (blue - red) * 60 / diff + 120
		elif max_val == blue: hue = (red - green) * 60 / diff + 240
	return [hue, saturation, velocity]

def HSV2RGB(hue, saturation, velocity):
	cc_i = hue / 6.0
	cc_ir = int((cc_i - math.floor(cc_i)))
	p = int(velocity * (255 - saturation) / 255)
	q = int(velocity * (255 - cc_ir * saturation) / 255)
	t = int(velocity * (255 - (1.0 - cc_ir) * saturation) / 255)
	red = green = blue = velocity
	
	rem = int(math.floor(cc_i)) % 6
	if rem == 0:
		green = t
		blue = p
	elif rem == 1:
		red = q
		blue = p
	elif rem == 2:
		red = p
		blue = t
	elif rem == 3:
		red = p
		green = q
	elif rem == 4:
		red = t
		green = p
	elif rem == 5:
		green = p
		blue = q
	return [red, green, blue]



# RGB<>CMYK color conversion
def RGB2CMYK(red, green, blue):
	black = 1.0 - _max(red, green, blue)
	cyan = (1.0 - red - black) / (1.0 - black)
	magenta = (1.0 - green - black) / (1.0 - black)
	yellow = (1.0 - blue - black) / (1.0 - black)
	return [cyan, magenta, yellow, black]

def CMYK2RGB(cyan, magenta, yellow, black):
	red = (1.0 - cyan) / (1.0 - black)
	green = (1.0 - magenta) / (1.0 - black)
	blue = (1.0 - yellow) / (1.0 - black)
	return [red, green, blue]

# RGB<>YIQ color conversion
def RGB2YIQ(red, green, blue):
	yluma = 0.299 * red + 0.587 * green + 0.114 * blue
	inphase = 0.569 * red - 0.275 * green - 0.322 * blue
	quadrature = 0.211 * red - 0.523 * green + 0.312 * blue
	return [yluma, inphase, quadrature]

def YIQ2RGB(yluma, inphase, quadrature):
	red = yluma + 0.956 * inphase + 0.621 * quadrature
	green = yluma - 0.272 * inphase - 0.647 * quadrature
	blue = yluma - 1.106 * inphase + 1.703 * quadrature
	return [red, green, blue]

def XYZ2H(cc_q):
	if cc_q > 0.008856: return cc_q**0.333333
	return 7.787 * cc_q + 0.137931

# RGB<>XYZ color conversion
def RGB2XYZ(red, green, blue):
	adapt = 0.003922
	xresponse = (0.412424 * red + 0.357579 * green + 0.180464 * blue) * adapt
	yluminance = (0.212656 * red + 0.715158 * green + 0.072186 * blue) * adapt
	zblue = (0.019332 * red + 0.119193 * green + 0.950444 * blue) * adapt
	return [xresponse, yluminance, zblue]

def XYZ2RGB(xresponse, yluminance, zblue):
	red = xresponse * 3.080342 - yluminance * 1.537399 - zblue * 0.542943
	green = xresponse * -0.921178 + yluminance * 1.87593 + zblue * 0.045248
	blue = xresponse * 0.052881 - yluminance * 0.204011 + zblue * 1.15113
	return [red, green, blue]

# XYZ<>LAB color conversion
def XYZ2LAB(xresponse, yluminance, zblue):
	luminosity = 116 * XYZ2H(yluminance) - 16
	apoint = 500 * (XYZ2H(xresponse / 0.950467) - XYZ2H(yluminance))
	bpoint = 200 * (XYZ2H(yluminance) - XYZ2H(zblue / 1.088969))
	return [luminosity, apoint, bpoint]

def LAB2XYZ(luminosity, apoint, bpoint):
	YLUMINANCE = luminosity * (0.00862) + 0.137931
	XRESPONSE = apoint * (0.002) + YLUMINANCE
	ZBLUE = bpoint * (-0.005) + YLUMINANCE

	if XRESPONSE > 0.206897: xresponse = pow(XRESPONSE, 3)
	else: xresponse = XRESPONSE * (0.128419) - 0.017713
	if luminosity > 8: yluminance = pow(YLUMINANCE, 3)
	else: yluminance = luminosity * (0.00110705646)
	if ZBLUE > 0.206897: zblue = pow(ZBLUE, 3)
	else: zblue = ZBLUE * (0.128419) - 0.017713
	return [xresponse, yluminance, zblue]



# # RGB<>XYZ<>LAB color conversion
# void ColorConverter::RGB2LAB(int red, int green, int blue, double *luminosity, double *apoint, double *bpoint) {
# 	double xresponse, yluma, zblue;
# 	RGB2XYZ(red, green, blue, &xresponse, &yluma, &zblue);
# 	XYZ2LAB(xresponse, yluma, zblue, luminosity, apoint, bpoint);
# }

# void ColorConverter::LAB2RGB(double luminosity, double apoint, double bpoint, int *red, int *green, int *blue) {
# 	double xresponse, yluma, zblue;
# 	LAB2XYZ(luminosity, apoint, bpoint, &xresponse, &yluma, &zblue);
# 	XYZ2RGB(xresponse, yluma, zblue, red, green, blue);
# }

# # HSL<>RGB<>HSV color conversion
# void ColorConverter::HSL2HSV(double hue, double saturation, double luminosity, double *_hue, double *_saturation, double *velocity) {
# 	double red, green, blue;
# 	HSL2RGB(hue, saturation, luminosity, &red, &green, &blue);
# 	RGB2HSV(red, green, blue, _hue, _saturation, velocity);
# }

# void ColorConverter::HSV2HSL(double hue, double saturation, double velocity, double *_hue, double *_saturation, double *luminosity) {
# 	double red, green, blue;
# 	HSV2RGB(hue, saturation, velocity, &red, &green, &blue);
# 	RGB2HSL(red, green, blue, _hue, _saturation, luminosity);
# }

# # HSL<>RGB<>CMYK color conversion
# void ColorConverter::HSL2CMYK(double hue, double saturation, double luminosity, double *cyan, double *magenta, double *yellow, double *black) {
# 	double red, green, blue;
# 	HSL2RGB(hue, saturation, luminosity, &red, &green, &blue);
# 	RGB2CMYK(red, green, blue, cyan, magenta, yellow, black);
# }

# void ColorConverter::CMYK2HSL(double cyan, double magenta, double yellow, double black, double *hue, double *saturation, double *luminosity) {
# 	double red, green, blue;
# 	CMYK2RGB(cyan, magenta, yellow, black, &red, &green, &blue);
# 	RGB2HSL(red, green, blue, hue, saturation, luminosity);
# }

# # HSV<>RGB<>CMYK color conversion
# void ColorConverter::HSV2CMYK(double hue, double saturation, double velocity, double *cyan, double *magenta, double *yellow, double *black) {
# 	double red, green, blue;
# 	HSV2RGB(hue, saturation, velocity, &red, &green, &blue);
# 	RGB2CMYK(red, green, blue, cyan, magenta, yellow, black);
# }

# void ColorConverter::CMYK2HSV(double cyan, double magenta, double yellow, double black, double *hue, double *saturation, double *velocity) {
# 	double red, green, blue;
# 	CMYK2RGB(cyan, magenta, yellow, black, &red, &green, &blue);
# 	RGB2HSV(red, green, blue, hue, saturation, velocity);
# }

# # HSL<>RGB<>YIQ color conversion
# void ColorConverter::HSL2YIQ(double hue, double saturation, double luminosity, double *yluma, double *inphase, double *quadrature) {
# 	double red, green, blue;
# 	HSL2RGB(hue, saturation, luminosity, &red, &green, &blue);
# 	RGB2YIQ(red, green, blue, yluma, inphase, quadrature);
# }

# void ColorConverter::YIQ2HSL(double yluma, double inphase, double quadrature, double *hue, double *saturation, double *luminosity) {
# 	double red, green, blue;
# 	YIQ2RGB(yluma, inphase, quadrature, &red, &green, &blue);
# 	RGB2HSL(red, green, blue, hue, saturation, luminosity);
# }

# # HSV<>RGB<>YIQ color conversion
# void ColorConverter::HSV2YIQ(double hue, double saturation, double velocity, double *yluma, double *inphase, double *quadrature) {
# 	double red, green, blue;
# 	HSV2RGB(hue, saturation, velocity, &red, &green, &blue);
# 	RGB2YIQ(red, green, blue, yluma, inphase, quadrature);
# }

# void ColorConverter::YIQ2HSV(double yluma, double inphase, double quadrature, double *hue, double *saturation, double *velocity) {
# 	double red, green, blue;
# 	YIQ2RGB(yluma, inphase, quadrature, &red, &green, &blue);
# 	RGB2HSV(red, green, blue, hue, saturation, velocity);
# }

# # CMYK<>RGB<>YIQ color conversion
# void ColorConverter::CMYK2YIQ(double cyan, double magenta, double yellow, double black, double *yluma, double *inphase, double *quadrature) {
# 	double red, green, blue;
# 	CMYK2RGB(cyan, magenta, yellow, black, &red, &green, &blue);
# 	RGB2YIQ(red, green, blue, yluma, inphase, quadrature);
# }

# void ColorConverter::YIQ2CMYK(double yluma, double inphase, double quadrature, double *cyan, double *magenta, double *yellow, double *black) {
# 	double red, green, blue;
# 	YIQ2RGB(yluma, inphase, quadrature, &red, &green, &blue);
# 	RGB2CMYK(red, green, blue, cyan, magenta, yellow, black);
# }



total_tests = 0
total_passed = 0
total_failed = 0

def test_check(i, o):
	return i[0] == o[0] and i[1] == o[1] and i[2] == o[2]

def test_converter(converter1, converter2, tests, checker=test_check):
	global total_tests, total_passed, total_failed

	passed = 0
	failed = 0

	print "Testing {0} -> {1} -> {0}...".format(converter1.__name__, converter2.__name__)
	for t in tests:
		comment = "(%s)" %t[3] if len(t) >= 4 else ""
		result1 = converter1(*t[0:3])
		result2 = converter2(*result1)
		if checker(t, result2):
			if False: print "Pass:", t[0:3], "-> %s() ->" %converter1.__name__, result1, "-> %s() ->" %converter2.__name__, result2, comment
			passed += 1
			total_passed += 1
		else:
			if False: print "FAIL:", t[0:3], "-> %s() ->" %converter1.__name__, result1, "-> %s() ->" %converter2.__name__, result2, comment
			failed += 1
			total_failed += 1
	print "Tests Passed: %d/%d (%d failed)\n" %(passed, len(tests), failed)
	total_tests += len(tests)

def rgb_hsl_test_check(i, o):
	return i[0] == o[0] and (i[1] == o[1] or (o[1] == 0 and (o[2] == 0 or o[2] == 255))) and i[2] == o[2]



step = 4

print " -=- INITIALIZING VARIABLES -=- \n"

rgb_hsl_tests = []
hsl_rgb_tests = []

print "RGB2HSL..."
for i1 in range(0, 255, step):
	for i2 in range(0, 255, step):
		for i3 in range(0, 255, step):
			rgb_hsl_tests.append([i1, i2, i3])

print "HSL2RGB..."
for i1 in range(0, 359, step):
	for i2 in range(0, 255, step):
		for i3 in range(0, 255, step):
			rgb_hsl_tests.append([i1, i2, i3])

print "\n -=- STARTING TESTS -=- \n"

test_converter(RGB2HSL, HSL2RGB, rgb_hsl_tests, rgb_hsl_test_check)
test_converter(HSL2RGB, RGB2HSL, hsl_rgb_tests)
# test_converter(RGB2HSL, HSL2RGB, [[255, 255, 255], [0, 0, 0], [255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 255, 255], [0, 0, 255], [255, 0, 255]], rgb_hsl_test_check)
# test_converter(HSL2RGB, RGB2HSL, [[0, 255, 255], [0, 0, 0], [60, 255, 127], [300, 255, 127], [40, 255, 127]])
# test_converter(RGB2HSV, HSV2RGB, [[255, 255, 255], [0, 0, 0], [255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 255, 255], [0, 0, 255], [255, 0, 255]])
# test_converter(HSV2RGB, RGB2HSV, [[0, 255, 255], [0, 0, 0], [60, 255, 255], [300, 255, 255], [40, 0, 255]])

print " -=- Total Tests Passed: %d/%d (%d failed) -=-\n" %(total_passed, total_tests, total_failed)
print " -=- TESTS COMPLETE -=- \n"
