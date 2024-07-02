from main import count_dots
import cv2

def test_count_dots():
    im = cv2.imread("./val/map/mVu4qnH2KnOZWl23.jpg")

    c, r = count_dots(im)

    assert c == 9
    assert r == 5

    im = cv2.imread("./val/xray/0m24hj1jHwlED0MA.jpg")

    c, r = count_dots(im)

    assert c == 3
    assert r == 0

    im = cv2.imread("./val/saturn/h8gNkhysOkitV9F6.jpg")

    c, r = count_dots(im)

    assert c == 2
    assert r == 0
