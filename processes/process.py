import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
from IPython.display import HTML
from processes.demo import load_checkpoints, make_animation
from skimage import img_as_ubyte
from moviepy.editor import *
import ffmpeg

class dame():

    def dane(self, ctx):
        source_image = imageio.imread(f"./saved/{ctx.message.id}.png")
        reader = imageio.get_reader("./processes/template/04.mp4")

        
        source_image = resize(source_image, (256, 256))[..., :3]

        fps = reader.get_meta_data()['fps']
        driving_video = []
        try:
            for im in reader:
                driving_video.append(im)
        except RuntimeError:
            pass
        reader.close()

        
        driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]

        generator, kp_detector = load_checkpoints(config_path='./processes/config/vox-256.yaml', 
                                checkpoint_path='./processes/template/vox-cpk.pth.tar')

        predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)

        imageio.mimsave(f'./generated/{ctx.message.id}1.mp4', [img_as_ubyte(frame) for frame in predictions], fps=fps)

        predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=False, adapt_movement_scale=True)

        vidclip = ffmpeg.input(f"./generated/{ctx.message.id}1.mp4")
        audclip = ffmpeg.input("./processes/template/final_5f285f6e5b283d0015b11acf_80535.mp3")

        out = ffmpeg.output(vidclip, audclip, f"./generated/{ctx.message.id}2.mp4")
        out.run()

    