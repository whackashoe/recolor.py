#!/usr/bin/env python2.7

import cv2
import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input', type=str, required=True,
                    help='input file like input.mp4')
parser.add_argument('--output', type=str,
                    help='output file like output.mp4')
parser.add_argument('--color', type=int, default=2,
                    help=("color theme choice, 0-11\n"
                    "0 cv2.COLORMAP_AUTUMN\n"
                    "1 cv2.COLORMAP_BONE\n"
                    "2 cv2.COLORMAP_JET\n"
                    "3 cv2.COLORMAP_WINTER\n"
                    "4 cv2.COLORMAP_RAINBOW\n"
                    "5 cv2.COLORMAP_OCEAN\n"
                    "6 cv2.COLORMAP_SUMMER\n"
                    "7 cv2.COLORMAP_SPRING\n"
                    "8 cv2.COLORMAP_COOL\n"
                    "9 cv2.COLORMAP_HSV\n"
                    "10 cv2.COLORMAP_PINK\n"
                    "11 cv2.COLORMAP_HOT"))
parser.add_argument('--window', type=bool, default=True,
                    help="show a window with the video")

args = parser.parse_args()

capture = cv2.VideoCapture(args.input)
success, frame = capture.read()
height, width, channels = frame.shape

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if int(major_ver)  < 3 :
    fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
else :
    fps = capture.get(cv2.CAP_PROP_FPS)

if args.output:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

if args.window:
    cv2.namedWindow("recolor.py", cv2.WINDOW_NORMAL)

while success:
    success, frame = capture.read()

    if not success:
        break

    im_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    im_color = cv2.applyColorMap(im_gray, args.color)

    if args.output:
        writer.write(im_color)

    if args.window:
        cv2.imshow("recolor.py", im_color)
        if(cv2.waitKey(1) & 0xFF) == ord('q'):
            break

writer.release()

if args.output:
    print "file saved to {}".format(args.output)

if args.window:
    cv2.destroyAllWindows()
