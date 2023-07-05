import os
import customtkinter
import dataclasses
import sqlalchemy

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Load models tables
from models.automobiles import *
from models.projects import *
from models.sys import *

from modules.syspl.models.syspl import *
from modules.sysfazenda.models.sysfazenda import *
from modules.sysdivida.models.sysdivida import *

from PIL import Image

# Db engine
DB_ENGINE = sqlalchemy.create_engine('sqlite:///sysma.db', echo=False)

# Relationship
# SysplHistory.syspldata = relationship("SysplData", order_by = SysplData.id, back_populates = "sysplhistory")

# Create all tables
Base.metadata.create_all(DB_ENGINE)


# Paths
IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
DOCUMENTS_FOLDER = os.path.join(os.path.expandvars('%USERPROFILE%'),'Documents', 'Sysma')

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
        light_image=Image.open(os.path.join(IMAGE_PATH, 'importassets.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'importassets.png')), 
        size=(96,126)   
    )

    IMPORT_RESOURCE = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'importresource.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'importresource.png')), 
        size=(96,126)   
    )

    SYSPL = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'SYSPL.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'SYSPL.png')), 
        size=(96,126)   
    )

    SYSFAZENDA = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'SYSFAZENDA.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'SYSFAZENDA.png')), 
        size=(96,126)   
    )

    SYSDIVIDA = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'SYSDIVIDA.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'SYSDIVIDA.png')), 
        size=(96,126)   
    )

    NEW_PROJECT = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'newprojecttransparent.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'newprojecttransparent.png')), 
        size=(96,126)   
    )

    UPSTREAM_DB = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'upstream_db.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'upstream_db.png')), 
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

    FOLDERCHECK = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'foldercheck.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'foldercheck.png')), 
        size=(21,21)   
    )

    FOLDERCHECKV2 = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'folder-check.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'folder-check.png')), 
        size=(87,87)   
    )

    UPLOADFILE = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'upload-file.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'upload-file.png')), 
        size=(87,87)   
    )

    BTN_CALENDAR = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'btn_img_calendar.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'btn_img_calendar.png')), 
        size=(26,26)   
    )

    BTN_MOD1 = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'mod1.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'mod1.png')), 
        size=(114, 230)   
 
    )

    BTN_MOD2 = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'mod2-disable.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'mod2-disable.png')), 
        size=(114, 230)   
 
    )

    BTN_MOD3 = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'mod3-disable.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'mod3-disable.png')), 
        size=(114, 230)   
    )

    BTN_ATTACH = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(IMAGE_PATH, 'attach.png')), 
        dark_image=Image.open(os.path.join(IMAGE_PATH, 'attach.png')), 
        size=(40, 40)   
    )

    ICON = os.path.join(IMAGE_PATH, 'favicon_transparent_32x32.ico')
    ICONV2 = os.path.join(IMAGE_PATH, 'icon.ico')

@dataclasses.dataclass
class Fonts:
    pass