from typing import Tuple
import datetime
from tkinter import Tk
from tkinter import StringVar
from tkinter import OptionMenu


def define_option_menu(
        master: Tk,
        option_list: list,
        default_index: int
) -> Tuple[OptionMenu, StringVar]:
    variable = StringVar(master)
    variable.set(option_list[default_index])
    option_menu = OptionMenu(master, variable, *option_list)
    option_menu.pack()
    return option_menu, variable


def get_time(fmt: str = '%H:%M:%S') -> str:
    return datetime.datetime.now().strftime(fmt)
