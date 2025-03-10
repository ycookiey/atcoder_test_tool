import tkinter as tk
from core.app import AtCoderTestTool


def main():
    root = tk.Tk()
    app = AtCoderTestTool(root)

    # ウィンドウ閉じる時のイベントを設定
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()
