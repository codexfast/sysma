import os
import customtkinter
import dataclasses

from PIL import Image

# Paths
IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
DOCUMENTS_FOLDER = os.path.join(os.path.expandvars('%USERPROFILE%'),'Documents')


# Imgs

@dataclasses.dataclass
class Images:
    RIGHT_BG = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'right-bg-II.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'right-bg-II.png')), 
        size=(419, 450)    
    )
    
    LEFT_BG = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'left-bg-II.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'left-bg-II.png')), 
        size=(181, 450)    
    )

    LABEL = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'sysma-high-label.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'sysma-high-label.png')), 
        size=(89,19)   
    )

    IMPORT_EXCEL = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'import_xlsx.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'import_xlsx.png')), 
        size=(96,132)   
    )

    EXPORT_EXCEL = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'export_xlsx.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'export_xlsx.png')), 
        size=(96,132)   
    )
 

    NEW_PROJECT = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'newprojecttransparent.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'newprojecttransparent.png')), 
        size=(96,126)   
    )

    PROJECTS = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'projects.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'projects.png')), 
        size=(96,126)   
    )

    CONFIG = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'config.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'config.png')), 
        size=(96,126)   
    )

    DASHBOARD = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'dashboard.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'dashboard.png')), 
        size=(96,126)   
    )

    ICON = os.path.join(IMAGE_PATH, 'favicon_transparent_32x32.ico')

@dataclasses.dataclass
class Fonts:
    pass