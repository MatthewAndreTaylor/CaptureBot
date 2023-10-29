import cv2
import os


def lapse(image_dir: str):
    images = [img for img in os.listdir(image_dir) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_dir, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(f"{image_dir}.mp4", fourcc, 120, (width, height))

    for image in images:
        image_path = os.path.join(image_dir, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    video.release()


lapse("timelapse")
