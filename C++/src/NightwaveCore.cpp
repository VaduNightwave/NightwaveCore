//
// Nightwave Core - NightwaveCore.cpp
// ©2017 Nightwave Studios: Vinyl Darkscratch, Light Apacha.
// https://www.nightwave.co/
//

#include "NightwaveCore.h"

#include <string>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <cmath>
#include <cassert>

#ifdef OSX_BUNDLE
	#include <CoreFoundation/CoreFoundation.h>
#endif

std::string ResourceBase;

void setResourceBase(const char *resource_base) {
	ResourceBase = std::string(resource_base);
}

// Mac app bundle vs. unbundled executable resource obtainer
std::string getResourcePath(const char *resource_name) {
#ifdef OSX_BUNDLE
	if (ResourceBase == "") {
		CFStringRef resourceName = CFStringCreateWithCString(NULL, resource_name, kCFStringEncodingUTF8);
		CFURLRef appUrlRef = CFBundleCopyResourceURL(CFBundleGetMainBundle(), resourceName, NULL, NULL);
		CFRelease(resourceName);
		if (appUrlRef == NULL) return std::string(resource_name);
		CFStringRef filePathRef = CFURLCopyPath(appUrlRef);
		std::string filePath(CFStringGetCStringPtr(filePathRef, kCFStringEncodingUTF8));

		// Release references
		CFRelease(filePathRef);
		CFRelease(appUrlRef);

		return filePath;
	}
#endif
	assert(ResourceBase != "");
	return std::string(ResourceBase) + "/" + std::string(resource_name);
}

// Variable conversion
std::string to_padded_string(int value, int width) {
	std::ostringstream out;
	out << std::setfill('0') << std::setw(width) << value;
	return out.str();
}

std::string to_padded_string(double value, int width, int precision) {
	std::ostringstream out;
	out << std::setfill('0') << std::setw(width+precision) << std::setprecision(precision) << value;
	return out.str();
}

// Math helpers
double threeway_max(double val_a, double val_b, double val_c) {
	return max(val_a, max(val_b, val_c));
}

int threeway_max(int val_a, int val_b, int val_c) {
	return max(val_a, max(val_b, val_c));
}

double threeway_min(double val_a, double val_b, double val_c) {
	return min(val_a, min(val_b, val_c));
}

int threeway_min(int val_a, int val_b, int val_c) {
	return min(val_a, min(val_b, val_c));
}

double clamp(double val, double minimum, double maximum) {
	return max(minimum, min(val, maximum));
}

int clamp(int val, int minimum, int maximum) {
	return max(minimum, min(val, maximum));
}