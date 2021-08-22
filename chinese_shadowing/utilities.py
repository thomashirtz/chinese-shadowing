from tkinter import StringVar
from tkinter import OptionMenu
from tkinter import Tk


def define_option_menu(master: Tk, option_list: list, default_index: int):
    variable = StringVar(master)
    variable.set(option_list[default_index])
    option_menu = OptionMenu(master, variable, *option_list)
    option_menu.pack()
    return option_menu, variable
