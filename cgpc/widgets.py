#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import cmd


class ListBox(Gtk.Frame):
    def __init__(self):
        Gtk.Frame.__init__(self)
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.pkg_image = Gtk.Image()
        self.name_label = Gtk.Label()
        self.category_label = Gtk.Label()
        self.version_label = Gtk.Label()

        self.box.pack_start(self.pkg_image, False, False, 5)
        self.box.pack_start(self.name_label, False, False, 5)
        self.box.pack_end(self.category_label, False, False, 5)
        self.box.pack_end(self.version_label, False, False, 5)

        self.add(self.box)

    def set_data(self, name: str, category: str = ""):
        pixbuf = Gtk.IconTheme.get_default().load_icon("muon", 48, 0)

        self.pkg_image.set_from_pixbuf(pixbuf)
        self.name_label.set_text(name)
        self.category_label.set_text(category)

        version_output = cmd.get_pkg_best_version(category, name)[0]
        version_text = version_output.split(" | ")[1].split(": ")[1]
        self.version_label.set_text(version_text)


class ListViewWidget(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.upper_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.stack = Gtk.Stack()
        self.stack.set_border_width(5)
        self.pack_start(self.upper_box, False, False, 0)
        self.pack_start(self.stack, True, True, 0)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)
        self.list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.list_box.set_border_width(10)
        self.scrolled_window.add(self.list_box)

        self.stack.add_named(self.scrolled_window, "list")

    def add_items(self, items_list):
        for item in items_list:
            widget = ListBox()

            name = item.split("/")[1]
            category = item.split("/")[0]

            widget.set_data(name=name, category=category)

            self.list_box.pack_start(widget, True, True, 0)

