#! /usr/bin/python3

# Author Sarvesh Bhatnagar

from PIL import Image
import argparse
import os
from typing import List, Tuple

class LoadImages:
    """
    Class Responsible for Loading Images from the directory.

    Attributes:
        datapath: The path to the directory containing the images
        image_names: The list of image names
        images: The list of images
        type: The type of the images
    
    Methods:
        load_image_names: Loads all the image names from the directory
        load_images: Loads all the images from the directory
        get_images: Returns the list of images
        get_image_names: Returns the list of image names
        get_image_count: Returns the number of images
        get_image_name: Returns the name of the image at the given index
        get_image: Returns the image at the given index

    """
    def __init__(self, path, tp="jpg") -> None:
        self.datapath = path
        self.tp = tp
        self.image_names = self.load_image_names()
        self.images = self.load_images()
        self.image_count = self.get_image_count()
        self.combined_height = self.get_combined_height()



    def get_combined_height(self) -> int:
        """
        Returns the combined height of all the images

        params: None
        return: int
        """
        return sum([image.height for image in self.images])

    def load_image_names(self) -> List[str]:
        """
        Loads all the image names from the directory

        params: None
        return: List[str]
        """
        image_names = []
        for filename in os.listdir(self.datapath):
            if filename.endswith(".{}".format(self.tp)):
                image_names.append(filename)
        self.image_names = image_names
        return self.image_names

    def load_images(self) -> List[Image.Image]:
        """
        Loads all the images from the directory

        params: None
        return: List[Image.Image]
        """
        images = []
        for filename in self.image_names:
            images.append(Image.open(os.path.join(self.datapath, filename)))
        
        self.images = images
        return images

    def get_images(self) -> List[Image.Image]:
        """
        Returns the list of images

        params: None
        return: List[Image.Image]
        """
        return self.images

    def get_image_names(self) -> List[str]:
        """
        Returns the list of image names

        params: None
        return: List[str]
        """
        return self.image_names

    def get_image_count(self) -> int:
        """
        Returns the number of images

        params: None
        return: int
        """
        return len(self.images)
    
    def get_image_name(self, index: int) -> str:
        """
        Returns the name of the image at the given index

        params: int
        return: str
        """
        return self.image_names[index]

    def get_image(self, index: int) -> Image.Image:
        """
        Returns the image at the given index

        params: int
        return: Image.Image
        """
        return self.images[index]
    
    

    

class ImageProcessor(LoadImages):
    def __init__(self, path, tp) -> None:
        super().__init__(path, tp=tp)
        self.tp = tp
        self.max_width, self.max_height = self.get_max_size_image()
        self.processed_images= self.change_images()


    def get_max_size_image(self) -> Tuple[int,int]:
        """
        Returns the max width and max hight among all images.

        Time Complexity: O(n)

        params: none
        returns Tuple(int,int)
        """

        max_width = 0
        max_height = 0
        for image in self.images:
            if image.width > max_width:
                max_width = image.width
            if image.height > max_height:
                max_height = image.height

        return (max_width, max_height)

    
    def change_image_size_by_filling(self, image: Image.Image, width: int, height: int) -> Image.Image:
        """
        Changes the size of the image to the given width and height.
        Does not change proportions.
        Just adds white background to the image.

        Code Credits : https://stackoverflow.com/questions/44370469/python-image-resizing-keep-proportion-add-white-background

        Time Complexity: O(1)

        params: Image, width, height
        returns Image
        """
        image_size = image.size
        background = Image.new('RGBA', (width, image_size[1]), (255, 255, 255, 255))
        offset = ((width - image_size[0]) // 2, (height - image_size[1]) // 2)

        background.paste(image, offset)
        return background

    def change_images(self):
        """
        Change all image by applying the required transformations.

        Can be updated but currently we are only applying the background transformation

        """
        same_size_images = []
        for image in self.images:
            image = self.change_image_size_by_filling(image, self.max_width, image.height)
            same_size_images.append(image)

        return same_size_images

    def stitch_images(self, images: List[Image.Image], width: int, height: int) -> Image.Image:
        """
        Stitches the images together to form a single image.

        Time Complexity: O(n)

        params: List[Image.Image], width, height
        returns Image.Image
        """
        stitched_image = Image.new('RGB', (width, height))
        offset = 0
        for image in images:
            stitched_image.paste(image, (0, offset))
            offset += image.height

        return stitched_image

    def get_stitched_image(self) -> Image.Image:
        """
        Returns the stitched image

        params: None
        returns Image.Image
        """
        return self.stitch_images(self.processed_images, self.max_width, self.combined_height)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quick Notes")
    parser.add_argument("path", type=str, help="Path to the directory containing the images")
    parser.add_argument("-tp", type=str, default="png", help="Type of the images")
    parser.add_argument("-out", type=str, default="stitched.pdf", help="Name of the output file")


    args = parser.parse_args()

    pth = args.path
    tp = args.tp
    ip = ImageProcessor(pth, tp)
    stitched_image = ip.get_stitched_image()
    stitched_image.save(os.path.join(pth, args.out))
    