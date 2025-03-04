import tkinter as tk
from core.app import AtCoderTestTool


def main():
    root = tk.Tk()
    app = AtCoderTestTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()
