import cv2
import numpy as np


def resize_and_show(title, image, show, scale=0.2):
    if not show:
        return
    """Resizes the image and displays it."""
    height, width = image.shape[:2]
    resized = cv2.resize(image, (int(width * scale), int(height * scale)))
    cv2.imshow(title, resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def preprocess_image(image_path, args= None, show = False):
    """Loads and preprocesses the image for peg detection."""
    print("Start processing image")
    if args is None:
        args = [{"Mask" : True}]

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    resize_and_show("Original Image", image, show)

    image_transformed = image

    for trans in args:
        image_transformed = transform_image(trans, image_transformed)
        resize_and_show("image_transformed", image_transformed, show)



    if "Mask" in args and args["Mask"]:
        # Detect circles using Hough Transform
        circles = cv2.HoughCircles(image_transformed, cv2.HOUGH_GRADIENT, dp=1.2, minDist=10000, param1=50, param2=30,
                                   minRadius=1000, maxRadius=2000)

        if circles is not None:
            circles = np.uint16(np.around(circles))
        else:
            print("No board detected.")
            return None
        x, y, r = circles[0][0]  # Take the first (largest) detected circle

        # Create a mask to extract only the circle
        mask = np.zeros_like(image_gray)
        cv2.circle(mask, (x, y), r - 150, 255, thickness=-1)
        # Apply mask
        image_transformed = cv2.bitwise_and(image_transformed, image_transformed, mask=mask)

        # Save & Show cropped image
        resize_and_show("Cropped Circle", image_transformed, show)

    circles = None
    if "Circles" in args and args["Circles"]:
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
            resize_and_show("Detected Pegs", output_image, show)
        else:
            print("error")

    return image_transformed, circles

def transform_image(args, image):
    print(args)
    image_transformed = image
    if "Gray" in args and args["Gray"]:
        image_transformed = cv2.cvtColor(image_transformed, cv2.COLOR_BGR2GRAY)

    if ("Blur" in args) and args["Blur"]:
        image_transformed = cv2.GaussianBlur(image_transformed, (5, 5), 0)

    if "Thresh" in args and args["Thresh"]:
        _, image_transformed = cv2.threshold(image_transformed, 100, 255, cv2.THRESH_BINARY_INV)

    if "thresh_adaptive" in args and args["thresh_adaptive"]:
        image_transformed = cv2.adaptiveThreshold(image_transformed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                  cv2.THRESH_BINARY, 11, 2)

    if "Canny" in args and args["Canny"]:
        print("Processing canny algorithm")
        # image_transformed = cv2.Canny(image_gray, 25, 200)
        # Apply Canny edge detection to each channel
        B, G, R = cv2.split(image_transformed)
        B_cny = cv2.Canny(B, 10, 150)
        G_cny = cv2.Canny(G, 10, 150)
        R_cny = cv2.Canny(R, 10, 150)

        # Merge the results
        image_transformed = cv2.merge([B_cny, G_cny, R_cny])

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))

    if "Erosion" in args and args["Erosion"]:
        image_transformed = erosion_image(image_transformed, kernel)
    if "Dilation" in args and args["Dilation"]:
        image_transformed = dilation_image(image_transformed, kernel)

    return image_transformed


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

