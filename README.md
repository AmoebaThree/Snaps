# Snaps

Image sensor

## Message spec

format: \<channel> "message"

**Inputs**

* \<snaps.pi> <filename>
  * Triggers the Pi camera to take a photo and store it as filename
  * Location of image capture to be determined
* \<snaps.cam> <filename>
  * Triggers the webcam to take a photo and store it as filename
  * Location of image capture to be determined

**Outputs**

* \<snaps.pi.capture> <filename>
  * Advises that a photo has been stored from the Pi camera with the specified filename
* \<snaps.cam.capture> <filename>
  * Advises that a photo has been stored from the webcam with the specified filename
