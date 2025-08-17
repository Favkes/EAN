from gui.core import App
import tkinter as tk


def main():
    root = tk.Tk()
    root.geometry("700x500")
    root.minsize(400, 300)
    root.maxsize(800, 600)
    root.config(
        padx=5, pady=5
    )

    app = App(root)
    app.build()
    app.display()


if __name__ == "__main__":
    main()
