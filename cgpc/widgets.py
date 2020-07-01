#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import cmd

from . import cmd


class AppWidget(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.app_name_box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.information_box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.description_box = Gtk.Box(Gtk.Orientation.HORIZONTAL)

        self.pkg_image = Gtk.Image()
        self.app_name = Gtk.Label()

        self.category = self.InfoBox("Category:")
        self.home_page_url = self.InfoBox("Home page:")
        self.version_label = self.InfoBox("Version:")
        self.license_label = self.InfoBox("License(s):")

        self.description_textview = Gtk.TextView()
        self.description_textview.set_editable(False)

        self.app_name_box.pack_start(self.pkg_image, False, False, 3)
        self.app_name_box.pack_start(self.app_name, False, False, 3)

        self.information_box.pack_start(self.category, True, True, 3)
        self.information_box.pack_start(self.home_page_url, True, True, 3)
        self.information_box.pack_start(self.version_label, True, True, 3)
        self.information_box.pack_start(self.license_label, True, True, 3)

        self.description_box.pack_start(self.description_textview, True, True, 3)

        self.pack_start(self.app_name_box, False, False, 2)
        self.pack_start(self.information_box, False, True, 2)
        self.pack_start(self.description_box, True, True, 2)

    def info_box(self, header):
        frame = Gtk.Frame()
        box = Gtk.Box(Gtk.Orientation.VERTICAL)
        header_label = Gtk.Label(label=header)
        data_label = Gtk.Label()

        box.pack_start(header_label, True, True, 0)
        box.pack_start(data_label, True, True, 0)

        frame.add(box)

        return frame

    def set_data(self, name: str, category: str):
        pixbuf = Gtk.IconTheme.get_default().load_icon("muon", 48, 0)
        self.pkg_image.set_from_pixbuf(pixbuf)
        self.app_name.set_text(name)
        self.category.set_text(category)

        app_information = cmd.get_app_information(category, name)[0]
        app_info_list = app_information.split(" | ")
        version_text = app_info_list[1].split(": ")[1]
        license_text = app_info_list[2].split(": ")[1]
        homepage_text = app_info_list[3].split(": ")[1]
        description = app_info_list[4].split(": ")[1]

        self.version_label.set_text(version_text)
        self.license_label.set_text(license_text)
        self.home_page_url.set_text(homepage_text)
        tbuffer = self.description_textview.get_buffer()
        tbuffer.set_text(description)

    class InfoBox(Gtk.Frame):
        def __init__(self, header):
            Gtk.Frame.__init__(self)

            self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.header_label = Gtk.Label(label=header)
            self.data_label = Gtk.Label()

            self.box.pack_start(self.header_label, False, False, 2)
            self.box.pack_start(self.data_label, True, True, 2)

            self.add(self.box)

        def set_text(self, text):
            self.data_label.set_text(text)


class ListBox(Gtk.Frame):
    def __init__(self):
        Gtk.Frame.__init__(self)
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.pkg_image = Gtk.Image()
        self.name_label = Gtk.Label()
        self.view_button = Gtk.Button(label="View")
        self.category_label = Gtk.Label()
        self.version_label = Gtk.Label()

        self.box.pack_start(self.pkg_image, False, False, 5)
        self.box.pack_start(self.name_label, False, False, 5)
        self.box.pack_end(self.view_button, False, False, 5)
        self.box.pack_end(self.version_label, False, False, 5)
        self.box.pack_end(self.category_label, False, False, 5)

        self.add(self.box)

    def set_data(self, name: str, category: str = ""):
        pixbuf = Gtk.IconTheme.get_default().load_icon("muon", 48, 0)

        self.pkg_image.set_from_pixbuf(pixbuf)
        self.name_label.set_text(name)
        self.category_label.set_text("Category:\n" + category)

        version_output = cmd.get_pkg_best_version(category, name)[0]
        version_text = version_output.split(" | ")[1].split(": ")[1]
        self.version_label.set_text("Version:\n" + version_text)


class ListViewWidget(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.upper_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.back_button = Gtk.Button(label="Back")
        self.upper_box.pack_start(self.back_button, False, False, 3)
        self.back_button.set_sensitive(False)
        self.back_button.connect("clicked", self.return_list)

        self.stack = Gtk.Stack()
        self.stack.set_border_width(5)
        self.pack_start(self.upper_box, False, False, 0)
        self.pack_start(self.stack, True, True, 0)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)
        self.list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.list_box.set_border_width(10)
        self.scrolled_window.add(self.list_box)

        self.app_widget = AppWidget()

        self.stack.add_named(self.scrolled_window, "list")
        self.stack.add_named(self.app_widget, "app")

    def add_items(self, items_list):
        for item in items_list:
            widget = ListBox()

            name = item.split("/")[1]
            category = item.split("/")[0]

            widget.set_data(name=name, category=category)
            widget.view_button.connect("clicked", self.show_view_page, widget)

            self.list_box.pack_start(widget, True, True, 0)

    def return_list(self, button):
        button.set_sensitive(False)
        self.stack.set_visible_child_name("list")

    def show_view_page(self, event, widget):
        name = widget.name_label.get_text()
        category = widget.category_label.get_text()

        self.app_widget.set_data(name, category)
        self.stack.set_visible_child_name("app")
        self.app_widget.show_all()
        self.back_button.set_sensitive(True)
