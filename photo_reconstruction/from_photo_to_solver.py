import numpy as np

import photo_reco
import grid_reconstruction
import recreate_line

def from_photo_to_solver(path):
    processed_image, circles = photo_reco.preprocess_image(path, [{"Blur": True},{ "Gray": True},{ "Thresh": True},{"Dilatation": True},{"Erosion": True},{"Mask": True},{"Circles": True}], show = True)
    circles_p = photo_reco.from_circles_to_points(circles)
    circles_p = np.array(circles_p)
    lines = recreate_line.get_lines(circles_p, 7)
    lines_p = recreate_line.from_lines_to_list_of_points(lines)
    grid = grid_reconstruction.grid_reconstruction(lines_p)
    grid_reconstruction.print_grid(grid)



if __name__ == "__main__":
    from_photo_to_solver("../Data/PegSolitaire001.jpg")
    print("finished")

