import cv2
import numpy as np


def resize_and_show(title, image, scale=0.2):
    """Resizes the image and displays it."""
    height, width = image.shape[:2]
    resized = cv2.resize(image, (int(width * scale), int(height * scale)))
    cv2.imshow(title, resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def preprocess_image(image_path):
    """Loads and preprocesses the image for peg detection."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    resize_and_show("Original Image", image)

    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    resize_and_show("Blurred Image", blurred)

    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)
    resize_and_show("Thresholded Image", thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (50, 50))

    eroded_img = erosion_image(thresh, kernel)
    resize_and_show("Eroded Image", eroded_img)

    dilation_img = dilation_image(eroded_img, kernel)
    resize_and_show("Dilated Image", dilation_img)

    # Detect circles using Hough Transform
    circles = cv2.HoughCircles(dilation_img, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
                               param1=50, param2=30, minRadius=1000, maxRadius=2000)
    if circles is not None:
        circles = np.uint16(np.around(circles))
    else:
        print("No board detected.")
        return None
    x, y, r = circles[0][0]  # Take the first (largest) detected circle

    # Create a mask to extract only the circle
    mask = np.zeros_like(image)
    cv2.circle(mask, (x, y), r - 10, 255, thickness=-1)

    # Apply mask
    cropped_circle = cv2.bitwise_and(dilation_img, dilation_img, mask=mask)

    # Save & Show cropped image
    resize_and_show("Cropped Circle", cropped_circle)

    # Detect circles using Hough Transform
    circles = cv2.HoughCircles(cropped_circle, cv2.HOUGH_GRADIENT, dp=1.5, minDist=100, param1=50, param2=20, minRadius=70, maxRadius=150)

    board = np.full((7, 7), -1)  # Initialize board with -1 (invalid spaces)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        output_image = image
        max_circles = 0
        for x, y, r in circles[0, :]:
            if max_circles == 50:
                break
            max_circles+=1
            cv2.circle(output_image, (x, y), r, (0, 255, 0), 2)
        resize_and_show("Detected Pegs", output_image)
    else:
        print("error")
    return thresh, circles

def erosion_image(image, kernel):
    img_erosion = cv2.erode(image, kernel, iterations=2)
    return img_erosion

def dilation_image(image, kernel):
    img_dilation = cv2.dilate(image, kernel, iterations=2)
    return img_dilation



if __name__ == "__main__":
    image_path = "../Data/PegSolitaire002B.jpg"
    processed_image, circles = preprocess_image(image_path)

