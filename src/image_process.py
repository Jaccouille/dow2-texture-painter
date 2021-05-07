from PIL import (
    Image,
    ImageChops,
    ImageOps,
    ImageColor,
    ImageEnhance,
    ImageDraw,
)
from src.constant import (
    DEFAULT_IMG_SIZE,
    ColorOps
)


def create_placeholder_img():
    img = Image.new(
        mode="RGBA", size=(DEFAULT_IMG_SIZE, DEFAULT_IMG_SIZE), color="gray"
    )
    d1 = ImageDraw.Draw(img)
    d1.text(xy=(180, 256), fill="black", text="Image PlaceHolder")
    return img


def almostEquals(a, b, thres=5):
    return all(abs(a[i] - b[i]) < thres for i in range(len(a)))


class ImageWorkbench:
    def __init__(self):
        self.tem_channels = []
        self.tem_selected = []
        self.colors = []
        self.img_og_dif = create_placeholder_img()
        self.img_og_tem = create_placeholder_img()
        self.brightness = 40
        self.contrast = 100
        self.apply_alpha = False
        self.apply_dirt = False
        self.apply_spec = False
        self.use_alpha_composite = False
        self.color_op = ColorOps.OVERLAY.value

    def process_coloring(self):
        """Process image with current workspace setting
        """
        # Creating a copied image to work on
        self.img_workspace = self.img_og_dif.copy()
        for color, channel in zip(self.colors, self.tem_channels):
            rgb = ImageColor.getrgb(color)

            # Ignore gray value as they are default
            # TODO: is this neccessary?
            if rgb == (128, 128, 128):
                continue

            # Get grayscaled original img
            # TODO: useless variable as it is not altered
            gray_img = self.img_og_dif.copy()
            channel.convert("L")

            # Colorize grayscale image using channel as mask
            new_img = ImageOps.colorize(channel, (0, 0, 0), color).convert('RGBA')

            # Add alpha using channel as mask
            new_img.putalpha(channel)

            if self.color_op == ColorOps.OVERLAY.value:
                new_img = ImageChops.overlay(gray_img, new_img)
            elif self.color_op == ColorOps.MULTIPLY.value:
                new_img = ImageChops.multiply(gray_img, new_img)
            else:
                new_img = ImageChops.screen(gray_img, new_img)

            enhancer_contrast = ImageEnhance.Contrast(new_img)
            new_img = enhancer_contrast.enhance(self.brightness / 100)
            enhancer_brightness = ImageEnhance.Brightness(new_img)
            new_img = enhancer_brightness.enhance(self.contrast / 100)

            # Paste processed image part on the workspace one
            self.img_workspace.paste(new_img, mask=channel)

    def refresh_workspace(self):
        """Refresh the workspace image with current settings"""
        self.process_coloring()
        # Add black background, hiding transparent pixel
        background = Image.new("RGBA", self.img_workspace.size, (0, 0, 0))
        self.img_workspace = Image.alpha_composite(background, self.img_workspace)

        if self.apply_alpha:
            tmp = self.refresh_team_colour_img()
            tmp = ImageChops.invert(tmp)
            self.img_workspace.putalpha(tmp)

        if self.apply_dirt:
            self.img_workspace = Image.alpha_composite(
                self.img_workspace, self.img_dirt
            )
        if self.apply_spec:
            self.img_workspace = Image.alpha_composite(
                self.img_workspace, self.img_spec
            )
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
