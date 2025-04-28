import cv2
import numpy as np


def resize_and_show(title, image, scale=0.2):
    """Resizes the image and displays it."""
    height, width = image.shape[:2]
    resized = cv2.resize(image, (int(width * scale), int(height * scale)))
    cv2.imshow(title, resized)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


def preprocess_image(image_path, args= None, show = False):
    """Loads and preprocesses the image for peg detection."""
    if args is None:
        args = {"mask" : True}
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if show:
        resize_and_show("Original Image", image)

    image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if show:
        resize_and_show("Original Image", image_gray)

    image_transformed = image_gray
    if ("blur" in args) and args["blur"]:
        image_transformed = cv2.GaussianBlur(image_gray, (5, 5), 0)
        if show:
            resize_and_show("Blurred Image", image_transformed)

    if "thresh" in args and args["thresh"]:
        _, image_transformed = cv2.threshold(image_transformed, 100, 255, cv2.THRESH_BINARY_INV)
        if show:
            resize_and_show("Thresholded Image", image_transformed)

    if "thresh_adaptive" in args and args["thresh_adaptive"]:
        image_transformed = cv2.adaptiveThreshold(image_transformed, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)
        if show:
            resize_and_show("Thresholded Image", image_transformed)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (50, 50))

    if "erosion" in args and args["erosion"]:
        image_transformed = erosion_image(image_transformed, kernel)
        if show:
            resize_and_show("Eroded Image", image_transformed)
    if "dilation" in args and args["dilation"]:
        image_transformed = dilation_image(image_transformed, kernel)
        if show:
            resize_and_show("Dilated Image", image_transformed)

    # Detect circles using Hough Transform
    circles = cv2.HoughCircles(image_transformed, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=50, param2=30, minRadius=1000, maxRadius=2000)

    if circles is not None:
        circles = np.uint16(np.around(circles))
    else:
        print("No board detected.")
        return None
    x, y, r = circles[0][0]  # Take the first (largest) detected circle

    # Create a mask to extract only the circle
    mask = np.zeros_like(image_gray)
    cv2.circle(mask, (x, y), r - 10, 255, thickness=-1)

    if "mask" in args and args["mask"]:
        # Apply mask
        image_transformed = cv2.bitwise_and(image_transformed, image_transformed, mask=mask)

        # Save & Show cropped image
        if show:
            resize_and_show("Cropped Circle", image_transformed)

    # Detect circles using Hough Transform
    circles = cv2.HoughCircles(image_transformed, cv2.HOUGH_GRADIENT, dp=1.5, minDist=100, param1=50, param2=20, minRadius=70, maxRadius=150)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        output_image = image_gray
        max_circles = 0
        for x, y, r in circles[0, :]:
            if max_circles == 50:
                break
            max_circles+=1
            cv2.circle(output_image, (x, y), r, (0, 255, 0), 2)
        if show:
            resize_and_show("Detected Pegs", output_image)
    else:
        print("error")

    return image_transformed, circles

def erosion_image(image, kernel):
    img_erosion = cv2.erode(image, kernel, iterations=2)
    return img_erosion

def dilation_image(image, kernel):
    img_dilation = cv2.dilate(image, kernel, iterations=2)
    return img_dilation

def from_circles_to_points(circles):
    return [elem[0:2].tolist() for elem in circles[0]]


if __name__ == "__main__":
    image_path = "../Data/PegSolitaire002B.jpg"
    processed_image, circles = preprocess_image(image_path)

