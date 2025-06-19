# Kevin Kiralyfalvi
# March 23, 2025
# Camera Test

import cv2
from picamera2 import Picamera2
import numpy as np
from time import sleep, perf_counter
import threading
import os
import subprocess


def gunCameraLoop(cam):

    while True:
        fTimeStart = perf_counter()

        img = cam.capture_array()
        write_to_framebuffer(0, img)

        fTime = perf_counter() - fTimeStart
        print(f"Gun frametime: {fTime:.4f} sec, FPS: {1 / fTime:.2f}")


def thermCameraLoop(cam):

    while True:
        fTimeStart = perf_counter()

        img = cam.capture_array()
        print(img)
        write_to_framebuffer(2, img)

        fTime = perf_counter() - fTimeStart
        print(f"Thermal frametime: {fTime:.4f} sec, FPS: {1 / fTime:.2f}")


def driveCameraLoop(cam):

    while True:
        fTimeStart = perf_counter()

        _, img = cam.read()
        img = img[..., ::-1]  # Swaps the red and blue color channels
        write_to_framebuffer(1, img)

        fTime = perf_counter() - fTimeStart
        print(
            f"Drive frametime: {fTime:.4f} sec, FPS: {1 / fTime:.2f}", end="; "
        )  # End in a semicolon + a space because i dont want to make 2 lines for what can fit on 1


def rgb888_to_rgb565(rgb888_frame):
    # Extract the R, G, B components from the 24-bit image
    r = (rgb888_frame[:, :, 0] >> 3).astype(
        np.uint16
    )  # For EVERY row, for EVERY column, take the first channel (red) and move it right 3
    g = (rgb888_frame[:, :, 1] >> 2).astype(
        np.uint16
    )  # For EVERY row, for EVERY column, take the second channel (green) and move it right 2
    b = (rgb888_frame[:, :, 2] >> 3).astype(
        np.uint16
    )  # For EVERY row, for EVERY column, take the third channel (blue) and move it right 3
    # Moving it right n times is the same as slicing off the last n bits. Since it's 5 6 5, take 8 8 8, remove 3 bits from red, remove 2 bits from green, and remove 3 bits from blue

    # Combine the components. Shift red over 11 so that the end (what was 5) now rests on spot 16. Shift green over 5 so that the end now rests right where red ends (11). Blue is 5 long, so automatically rests on 11 minus 6.
    rgb565_frame = (r << 11) | (g << 5) | b
    return rgb565_frame


def write_to_framebuffer(fb, image):
    # Takes a framebuffer id, appends it to a path, and open that path in writing in binary. Proceed to write to it.
    with open(("/dev/fb" + str(fb)), "wb") as buf:
        buf.write(rgb888_to_rgb565(image))


def getDriveCamAndInit():
    videoIDs = subprocess.run(  # List video devices and save them
        ["v4l2-ctl", "--list-devices"], capture_output=True, text=True
    )
    videoIDs = videoIDs.stdout
    loc = videoIDs.find(
        "046d:0825"
    )  # This is the model of my USB camera. If i use two of the same model, i will have to find a new way to do this
    if loc != -1:  # If it's not found (i.e. not plugged in), quit.
        # First, in the string of videoIDs, find first index the first instance of "video" after the index of my ID. Then, add 5 to that index which gives the index of the id following just after "video". Then, since im slicing from a string, convert to an int.
        driveCamID = int(videoIDs[videoIDs.find("video", loc) + 5])
    else:
        print("Could not find drive camera! Exiting!")
        exit()

    camDrive = cv2.VideoCapture(driveCamID)
    camDrive.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Set the width, then the height
    camDrive.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    # Brightness, contrast, saturation and such are personal preference. Backlight compensation is good for sillouettes against the sun. Auto exposure and exposure dynamic framerate ONLY work together. They must BOTH be active for auto exposure.
    os.system(
        f"v4l2-ctl -d /dev/video{driveCamID} --set-ctrl brightness=128 --set-ctrl contrast=64 --set-ctrl saturation=80 --set-ctrl gain=0 --set-ctrl sharpness=255 --set-ctrl backlight_compensation=1 --set-ctrl auto_exposure=3 --set-ctrl exposure_dynamic_framerate=1"
    )

    return camDrive


def getGunCamAndInit():
    camGun = Picamera2()  # Use the default class initialization for camGun
    config = camGun.create_video_configuration(  # Set the WIDTH, HEIGHT. Then, set to the color standard to the default with the key exception that the blue and red channels are swapped. Also, use 3 buffers. 2 is around 28fps, and 3 is 30fps.
        main={"size": (320, 240), "format": "BGR888"}, buffer_count=3
    )
    camGun.configure(config)  # Configure the object with the config we just created
    camGun.start()  # Start the camera

    return camGun


def getThermCamAndInit():
    camTherm = cv2.VideoCapture("video3")

    return camTherm


def main():

    camDrive = getDriveCamAndInit()
    camGun = getGunCamAndInit()
    camTherm = getThermCamAndInit()

    # Threading as a daemon so we can run both in sync (and to help when it desyncs so they are independent)
    threading.Thread(target=gunCameraLoop, args=(camGun,), daemon=True).start()
    threading.Thread(target=driveCameraLoop, args=(camDrive,), daemon=True).start()
    threading.Thread(target=thermCameraLoop, args=(camTherm,), daemon=True).start()

    # Do nothing forever, I just need to keep the main alive.
    while True:
        sleep(1)


main()
