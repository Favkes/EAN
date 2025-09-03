"""
Main running file of the app.

Contains the definition of the app's root window and initialization of core.App, that further handles
all application processes.
"""


from gui.core import App
import tkinter as tk


def main():
    """
    Initialize the root window and gui.App, build the App and display inside the window.

    :return: None
    """
    root = tk.Tk()
    root.title('EAN-NevLag25')
    root.geometry("700x500")
    root.minsize(400, 300)
    root.maxsize(800, 600)
    root.config(
        padx=5, pady=5
    )

    app = App(root)
    app.build()
    # app.debug_mode()
    app.display()


if __name__ == "__main__":
    main()
