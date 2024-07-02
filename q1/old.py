import cv2
import os
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)

PATH = "./test"
BLUE_MIN = (200, 0, 0)
BLUE_MAX = (255, 20, 20)
RED_MIN = (0, 0, 200)
RED_MAX = (20, 20, 255)
SOLUTION_PATH = "./output"


def contour_filtering(f):
    # Load image, grayscale, median blur, Otsus threshold
    image = cv2.imread(f)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 11)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    # Find contours and filter using contour area and aspect ratio
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        area = cv2.contourArea(c)
        if len(approx) > 5 and area > 10 and area < 500:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)

    # cv2.imshow('thresh', thresh)
    # cv2.imshow('opening', opening)
    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def circle_detection(im):
    # detect circles in the image
    circles = cv2.HoughCircles(
        im, cv2.HOUGH_GRADIENT, 10, 10, param1=1, param2=1, minRadius=0, maxRadius=0
    )
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(im, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(im, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        # show the output image
        cv2.imshow("Keypoints", im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return circles


def blob_detection(im) -> list:
    params = cv2.SimpleBlobDetector_Params()

    # Thresholds (default settings good enough for this task)
    # params.filterByColor = True
    # params.minThreshold = 200
    # params.maxThreshold = 255
    # params.filterByArea = False
    # params.minArea = 24
    # params.maxArea = 35
    # params.filterByCircularity = True
    # params.minCircularity = 0.87
    # params.filterByConvexity = False
    # params.minConvexity = 0.87
    # params.filterByInertia = False
    # params.minInertiaRatio = 0.01

    # for handling different version errors
    ver = (cv2.__version__).split(".")
    if int(ver[0]) < 3:
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(im)

    return keypoints


def find_contours(im):
    cnts = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    return cnts


def count_dots(im):
    # resize image to 200% for better blob detection
    h, w, _ = im.shape
    im = cv2.resize(im, (int(w * 4), int(h * 4)))

    blue_mask = cv2.inRange(im, BLUE_MIN, BLUE_MAX)
    blue_mask = 255 - blue_mask
    red_mask = cv2.inRange(im, RED_MIN, RED_MAX)
    red_mask = 255 - red_mask

    # len(keypoints) = number of red/blue dots
    blues = blob_detection(blue_mask)
    reds = blob_detection(red_mask)

    # im_with_both = cv2.drawKeypoints(im, reds, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # im_with_both = cv2.drawKeypoints(im_with_both, blues, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # cv2.imshow('im_with_both',im_with_both)
    # cv2.imshow('blue_mask',blue_mask)
    # cv2.imshow('red_mask',red_mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    column = len(reds) - 1  # -1 because zero-indexed
    row = len(blues) - 1

    return column, row


def main():
    for d in os.listdir(PATH):
        logging.info("Processing folder: " + d)

        puzzle_dir = os.path.join(PATH, d)
        height = None
        width = None
        cols = 0
        rows = 0

        puzzle_pieces = []

        for f in os.listdir(puzzle_dir):
            piece_filepath = os.path.join(puzzle_dir, f)
            piece_im = cv2.imread(piece_filepath)

            if height is None and width is None:
                height, width, _ = piece_im.shape

            c, r = count_dots(piece_im)

            # update total no of cols/rows
            cols = max(cols, c + 1)
            rows = max(rows, r + 1)

            puzzle_pieces.append((piece_im, c, r))

        logging.debug("Detected height: " + str(height))
        logging.debug("Detected width: " + str(width))
        logging.debug("Detected cols: " + str(cols))
        logging.debug("Detected rows: " + str(rows))

        # reconstruct puzzle
        # create new empty canvas of max cols * width, max rows * height
        puzzle_im = np.zeros((rows * height, cols * width, 3), np.uint8)
        logging.debug(puzzle_im.shape)

        for piece in puzzle_pieces:
            # y-first
            x = piece[1] * width
            x2 = x + width
            y = piece[2] * height
            y2 = y + height
            logging.debug(
                "x: "
                + str(x)
                + ", y: "
                + str(y)
                + ", x2: "
                + str(x2)
                + ", y2: "
                + str(y2)
            )

            puzzle_im[y:y2, x:x2] = piece[0]

        cv2.imshow("Reconstructed Puzzle", puzzle_im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    # piece_filepath = os.path.join("./val/map/mVu4qnH2KnOZWl23.jpg")
    # piece_im = cv2.imread(piece_filepath)

    # c, r = count_dots(piece_im)
