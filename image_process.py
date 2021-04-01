from PIL import (
    Image,
    ImageChops,
    ImageOps,
    ImageTk,
    ImageColor,
    ImageEnhance,
    ImageDraw,
)
from constant import (
    DEFAULT_IMG_SIZE,
)
import os

def create_placeholder_img():
    img = Image.new(
        mode="RGBA", size=(DEFAULT_IMG_SIZE, DEFAULT_IMG_SIZE), color="gray"
    )
    d1 = ImageDraw.Draw(img)
    d1.text(xy=(180, 256), fill="black", text="Image PlaceHolder")
    return img

def almostEquals(a,b,thres=5):
    return all(abs(a[i]-b[i])<thres for i in range(len(a)))

class ImageWorkbench():
    def __init__(self):
        self.tem_channels = []
        self.colors = []
        self.img_og_dif = create_placeholder_img()
        self.img_og_tem = create_placeholder_img()
        self.brightness = 40
        self.contrast = 100
        self.offset = 0

    def process_img(self, channel: Image, color: tuple):
        """Process image with current workspace setting

        :param channel: channel data selected from the tem file, used as a
        layer to colorize the image
        :type channel: Image
        :param color: RGBA Color used to colorize the image
        :type color: tuple
        :return: Processed Image
        :rtype: Image
        """
        img = ImageOps.colorize(channel, (0, 0, 0), color).convert("RGBA")
        # img = channel.convert("RGBA")

        # Apply transparency on black pixel
        # TODO: find efficient way to apply alpha on black pixel
        # pixeldata = list(img.getdata())
        # for i,pixel in enumerate(pixeldata):
        #     if almostEquals(pixel[:3], (0,0,0)):
        #         pixeldata[i] = (0, 0, 0, 0,)
        #     else:
        #         pixeldata[i] = color
        # img.putdata(pixeldata)

        enhancer_contrast = ImageEnhance.Contrast(img)
        img = enhancer_contrast.enhance(
            self.brightness / 100)
        enhancer_brightness = ImageEnhance.Brightness(img)
        img = enhancer_brightness.enhance(
            self.contrast / 100
        )
        return img

    def refresh_workspace(self):
        """Refresh the workspace image with current settings"""
        self.img_workspace = self.img_og_dif.copy()
        for color, channel in zip(self.colors, self.tem_channels):
            tmp = self.img_og_dif.copy()
            rgb = ImageColor.getrgb(color)
            if rgb != (128, 128, 128):
                channel.convert("L")
                processed_img = self.process_img(channel, rgb)
                # TODO: Improve following
                # multiply doesn't work with white color
                tmp = ImageChops.multiply(
                    tmp, processed_img)

                # Add works with white but not with black color
                self.img_workspace = ImageChops.add(self.img_workspace, tmp, offset=self.offset)
                # alpha_composite works with black but not white color
                # self.img_workspace.alpha_composite(tmp)

                # Debug
                # processed_img.save(os.curdir + f"/proc_{i}.png")
                # tmp.save(os.curdir + f"/tmp_{i}.png")
                # self.img_workspace.save(os.curdir + f"/work_{i}.png")

        background = Image.new("RGBA", self.img_workspace.size, (0, 0, 0))
        self.img_workspace = Image.alpha_composite(background, self.img_workspace)
        return self.img_workspace

    def refresh_team_colour_img(self, selection: tuple):
        new_img = Image.new("L", self.img_og_tem.size)
        if len(self.tem_channels) == 0:
            return self.img_og_tem
        for i in selection:
            # TODO: think about clean implementation
            try:
                new_img = ImageChops.add(new_img, self.tem_channels[i])
            except IndexError:
                return
        return new_img

    def apply_alpha(self, selection: list):
        """Takes selected channel layer and apply alpha on the workspace
        image"""
        for i in selection:
            alpha_mask = ImageChops.invert(self.tem_channels[i])
            self.img_workspace.putalpha(alpha_mask)

    def load_diffuse_file(self, filepath: str):
        """Load diffuse texture and set it as workspace image,

        :param filepath: path to file
        :type filepath: str
        """
        # IMG LOADER
        # Diffuse image
        self.img_og_dif = Image.open(filepath)
        # background = Image.new("RGBA", self.img_og_dif.size, (0, 0, 0))
        # self.img_og_dif = Image.alpha_composite(background, self.img_og_dif)

    def load_team_colour_file(self, filepath: str):
        self.img_og_tem = Image.open(filepath)
        self.tem_channels = self.img_og_tem.split()

    def save(self, filepath: str):
        self.img_workspace.save(filepath)
