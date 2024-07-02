# Solution Overview

1. Loop through folder path specified in main.py under `PATH` variable (at the top of the code).
2. For each folder path, loop through each nested directory for all pieces of a given puzzle (according to original files retrieved for the test).
3. For each puzzle piece, first determine the size of each puzzle piece by reading the first puzzle piece's shape.
4. Extract the mask of areas within the color range of red/blue dots (as provided in PDF) into 2 separate masks (1 for red, 1 for blue).
5. Do mask inversion, because blob detection somehow works better when the masks are inverted. `¯\_(ツ)_/¯`
6. Run blob detection on the red/blue masks respectively, returning a list containing detected blobs each.
7. Count the number of red/blue blobs detected; this will determine the position of the puzzle piece in the final reconstructed puzzle.
8. Update the maximum number of columns/rows accordingly.
9. After all puzzle pieces in a directory are processed, construct a canvas for the reconstructed puzzle using max cols * width, rows * height.
10. Replace each region of the puzzle with the respective puzzle piece.
11. Display the fully reconstructed puzzle on a GUI window (press any key to repeat for the next puzzle).

# Usage

All Python dependencies are captured in `requirements.txt`.

The folder structure expected for the script to work properly follows the original validation/test zips sent with this question:

```
<root>
  |- val *
    |- map
      |- <puzzle pieces>
    |- saturn
      |- <puzzle pieces>
    |- xray
      |- <puzzle pieces>
  |- test *
    |- fumo
      |- <puzzle pieces>
    |- galaxy
      |- <puzzle pieces>
    |- simple
      |- <puzzle pieces>
  |- main.py
  |- requirements.txt
  |- test_main.py
```

To run the script properly, simply set the `PATH` variable to a folder containing the nested folders for the puzzle pieces (marked with asterisk * above), followed by:

`python main.py`

# Assumptions

For this solution to work, the following assumptions are made:
- Each puzzle piece is of the same width/height (no irregular puzzle pieces).
- Each puzzle piece does not overlap with one another.
- Each of the dots do not overlap, or belong too close to one another (otherwise further scaling is needed).
- All puzzle pieces are neatly sorted into their own folders.

# Extras

I tried using contour filtering and circle detection via `cv2.HoughCircles` to minimal results. In the end blob detection worked the best for this usecase, so I decided to keep things simple and retain the use of blob detection.

There is a need to resize the images before running blob detection on it, as dots of the same color that are spaced close together would result in a single detection (instead of 2 separate detections), and mess up the reconstructed puzzle. Overall, I found that scaling the puzzle pieces to a factor of 4 provides the best blob detection rate over all validation/test cases provided in this case. I think scaling here is acceptable as its sole use is for determining the position of the puzzle piece - the scaled image is not used in the reconstruction process whatsoever. Less pixels = less compute :)

For the purposes of this experiment, only the following parameters are tuned:
- Size of puzzle piece prior to color range masking and blob detection
