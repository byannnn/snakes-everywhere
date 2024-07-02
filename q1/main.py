import cv2
import os
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

PATH = "./test"
BLUE_MIN = (200, 0, 0)
BLUE_MAX = (255, 20, 20)
RED_MIN = (0, 0, 200)
RED_MAX = (20, 20, 255)

def blob_detection(im) -> list:
    # Thresholds (default settings good enough for this task)
    params = cv2.SimpleBlobDetector_Params()

    # for handling different version errors
    ver = (cv2.__version__).split(".")
    if int(ver[0]) < 3:
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(im)

    return keypoints


def count_dots(im):
    # resize image to 400% for better blob detection
    h, w, _ = im.shape
    im = cv2.resize(im, (int(w * 4), int(h * 4)))

    # color range masking and inversion
    blue_mask = cv2.inRange(im, BLUE_MIN, BLUE_MAX)
    blue_mask = 255 - blue_mask
    red_mask = cv2.inRange(im, RED_MIN, RED_MAX)
    red_mask = 255 - red_mask

    # len(keypoints) = number of red/blue dots
    blues = blob_detection(blue_mask)
    reds = blob_detection(red_mask)

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

        # loop through each puzzle piece
        for f in os.listdir(puzzle_dir):
            piece_filepath = os.path.join(puzzle_dir, f)
            piece_im = cv2.imread(piece_filepath)

            # get shape of each puzzle piece
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

        # put the puzzle pieces according to their row/col
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
