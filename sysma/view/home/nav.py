import config
import customtkinter

class Navbar:
    def __init__(self, parent) -> None:

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(parent, corner_radius=0, width=40)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        customtkinter.CTkLabel(self.navigation_frame, text=None, image=config.Images.LEFT_BG).place(x=0, y=0)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, 
            text=None,
            image=config.Images.LABEL,
        )
        
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=(60,20))

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame, 
            corner_radius=0, 
            height=40, 
            border_spacing=10, 
            text="Principal",
            fg_color="transparent", 
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            width=106,
            font=customtkinter.CTkFont(size=14)
        )
        
        # self.home_button.grid(row=1, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame, 
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
            fg_color=("grey20"),
            # bg_color=("grey20"),
            button_color=("grey20")
        )
        
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
