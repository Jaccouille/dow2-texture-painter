from PIL import (
    Image,
    ImageChops,
    ImageOps,
    ImageColor,
    ImageEnhance,
    ImageDraw,
)
from dow2_texture_painter.constant import (
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


def almostEquals(a, b, thres=5):
    return all(abs(a[i]-b[i]) < thres for i in range(len(a)))


class ImageWorkbench():
    def __init__(self):
        self.tem_channels = []
        self.tem_selected = []
        self.colors = []
        self.img_og_dif = create_placeholder_img()
        self.img_og_tem = create_placeholder_img()
        self.brightness = 40
        self.contrast = 100
        self.offset = 0
        self.apply_alpha = False
        self.apply_dirt = False
        self.apply_spec = False
        self.use_alpha_composite = False

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

        # Apply transparency on black pixel
        # TODO: find efficient way to apply alpha on black pixel
        # if self.use_alpha_composite:
        colored = Image.new("RGBA", img.size, color)
        mask = ImageChops.invert(channel)
        img = Image.composite(img, colored, mask)
        img.putalpha(channel)

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
                tmp = ImageChops.multiply(
                    tmp, processed_img)

                # alpha_composite works with black but not white color
                if self.use_alpha_composite:
                    self.img_workspace.alpha_composite(tmp)
                # TODO: Improve following
                # multiply doesn't work with white color
                else:
                    # Add works with white but not with black color
                    self.img_workspace = ImageChops.add(
                        self.img_workspace, tmp, offset=self.offset)

                # Debug
                # processed_img.save(os.curdir + f"/proc_{i}.png")
                # tmp.save(os.curdir + f"/tmp_{i}.png")
                # self.img_workspace.save(os.curdir + f"/work_{i}.png")

        if self.apply_alpha:
            tmp = self.refresh_team_colour_img()
            tmp = ImageChops.invert(tmp)
            tmp.save(os.curdir + "/alpha.png")
            self.img_workspace.putalpha(tmp)

        if self.apply_dirt:
            self.img_workspace = Image.alpha_composite(
                self.img_workspace, self.img_dirt)
        if self.apply_spec:
            self.img_workspace = Image.alpha_composite(
                self.img_workspace, self.img_spec)
        # background = Image.new("RGBA", self.img_workspace.size, (0, 0, 0))
        # self.img_workspace = Image.alpha_composite(background, self.img_workspace)
        return self.img_workspace

    def refresh_team_colour_img(self):
        new_img = Image.new("L", self.img_og_tem.size)
        if len(self.tem_channels) == 0:
            return self.img_og_tem
        for i in self.tem_selected:
            # TODO: think about clean implementation
            try:
                new_img.paste(self.tem_channels[i], mask=self.tem_channels[i])
            except IndexError:
                return
        return new_img

    def load_diffuse_file(self, filepath: str):
        """Load diffuse texture and set it as workspace image,

        :param filepath: path to file
        :type filepath: str
        """
        self.img_og_dif = Image.open(filepath)

    def load_team_colour_file(self, filepath: str):
        self.img_og_tem = Image.open(filepath)
        self.tem_channels = self.img_og_tem.split()

    def load_dirt_file(self, filepath: str):
        self.img_dirt = Image.open(filepath)

    def load_specular_file(self, filepath: str):
        self.img_spec = Image.open(filepath)

    def save(self, filepath: str):
        self.img_workspace.save(filepath)
