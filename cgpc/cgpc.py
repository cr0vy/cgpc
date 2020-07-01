#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Custom Gentoo Package Center")
        self.set_size_request(1280, 720)

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.stack_widget = Gtk.Stack()
        self.stack_sidebar_widget = Gtk.StackSidebar()
        self.stack_sidebar_widget.set_stack(self.stack_widget)

        self.home_widget = HomeWidget()
        self.installed_widget = InstalledWidget()
        self.updates_widget = UpdatesWidget()

        self.stack_widget.add_titled(self.home_widget, "home", "Home")

        for category in ["Internet", "Chat", "Business", "Games", "Music", "Video", "Graphics", "Office", "Reading", "Development", "System"]:
            widget = CategoryWidget()
            self.stack_widget.add_titled(widget, category.lower(), category)

        self.stack_widget.add_titled(self.installed_widget, "installed", "Installed")
        self.stack_widget.add_titled(self.updates_widget, "updates", "Updates")

        self.box.pack_start(self.stack_sidebar_widget, False, False, 0)
        self.box.pack_start(self.stack_widget, True, True, 0)

        self.add(self.box)


class CategoryWidget(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)


class InstalledWidget(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)


class HomeWidget(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)


class UpdatesWidget(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)


def run():
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
