"""
Main running file of the app.

Contains the definition of the app's root window and initialization of core.App, that further handles
all application processes.
"""


from gui.core import App
import tkinter as tk
import ctypes


def main():
    """
    Initialize the root window and gui.App, build the App and display inside the window.

    :return: None
    """

    # Set the windows taskbar icon
    myappid = "favkescompany.favkesapp.v1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Initialize window
    root = tk.Tk()
    root.title('EAN-NevLag25')
    root.geometry("850x500")
    root.minsize(700, 400)
    root.maxsize(900, 600)
    root.config(
        padx=5, pady=5
    )
    root.iconbitmap("gui/icon.ico")

    # Initialize app
    app = App(root)
    app.build()
    # app.debug_mode()
    app.display()


if __name__ == "__main__":
    main()
