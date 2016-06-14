import re
from pyicloud import PyiCloudService

# For iCloud API
api = PyiCloudService('davidcai2012@gmail.com','cilantroLime7.03')
iphone = api.devices['cetbS6ENhf8TSwHWRSpwmcI8L3J+C3USnmt6gCjV05FdE2jKVT8dNeHYVNSUzmWV']

# For Jasper
WORDS = ["IPHONE", "FIND"]

def isValid(text):
	# Seperate, all valid triggers
	one = bool(re.search(r'\bIPHONE\b', text, re.IGNORECASE))
	two = bool(re.search(r'\bFIND\b', text, re.IGNORECASE))

	if one or two:
		return True
	else:
		return False

def handle(text, mic, profile):
	iphone.play_sound()
	mic.say("OK. Playing sound.")