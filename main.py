import tkinter as tk
from core.app import AtCoderTestTool


def main():
    root = tk.Tk()
    app = AtCoderTestTool(root)

    # ウィンドウ閉じる時のイベントを設定
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # グローバルホットキーの設定
    import keyboard

    def activate_window_handler():
        # Tkinterのメインスレッドで実行
        root.after(0, app.activate_window)

    # Alt+Hのホットキー設定
    keyboard.add_hotkey("alt+h", activate_window_handler)

    root.mainloop()


if __name__ == "__main__":
    main()
