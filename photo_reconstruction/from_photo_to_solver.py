import photo_reco
import grid_reconstruction
import recreate_line

def from_photo_to_solver(path):
    processed_image, circles = photo_reco.preprocess_image(path)

