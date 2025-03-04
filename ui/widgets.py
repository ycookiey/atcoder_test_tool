import tkinter as tk
from tkinter import scrolledtext
from ui.styles import COLOR_BG_LIGHT, COLOR_FG, COLOR_PRIMARY, COLOR_BG_DARK


def create_scrolledtext(parent, height=10, width=None, wrap=tk.WORD, readonly=False):
    """カスタマイズされたスクロールテキストウィジェットを作成"""
    text = scrolledtext.ScrolledText(parent, wrap=wrap, height=height, width=width)
    text.configure(
        bg=COLOR_BG_LIGHT,
        fg=COLOR_FG,
        insertbackground=COLOR_FG,
        selectbackground=COLOR_PRIMARY,
        selectforeground=COLOR_BG_DARK,
        borderwidth=1,
        highlightthickness=0,
        relief=tk.FLAT,
    )
    if readonly:
        text.configure(state="disabled")
    return text
