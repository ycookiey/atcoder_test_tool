import tkinter as tk
from core.app import AtCoderTestTool


def main():
    root = tk.Tk()
    app = AtCoderTestTool(root)

    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    import keyboard

    def activate_window_handler():
        # keyboardのコールバックは別のスレッドで呼ばれるため、Tkの操作をメインスレッドに渡す
        root.after(0, app.activate_window)

    keyboard.add_hotkey("alt+h", activate_window_handler)

    root.mainloop()


if __name__ == "__main__":
    main()
