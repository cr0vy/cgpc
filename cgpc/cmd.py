#!/usr/bin/env python3

import subprocess

available = []
installed = []


def get_app_information(category: str, name: str):
    app_pkg = None

    for pkg in available:
        if pkg.get_category() == category and pkg.get_name() == name:
            app_pkg = pkg
    
    return app_pkg


def get_available_pkgs(category: list):
    return_list = []

    for pkg in available:
        if pkg.get_category() in category:
            return_list.append(pkg)
    
    return return_list


def get_installed_list():
    return installed


def get_updates_list():
    return_list = []

    for pkg in installed:
        if pkg.is_update_available():
            return_list.append(pkg)

    return return_list


def update_pkg_list():
    p = subprocess.Popen(["eix", "-IC", "--format", '"Package: <installedversions:NAMEVERSION> | Newest: <bestversion:VERSION> | License: <licenses> | Homepage: <homepage> | Description: <description>\n"'], stdout=subprocess.PIPE, encoding="utf-8")
    out = p.stdout.readlines()

    for pkg in out:
        pkg = pkg.replace('"', "")
        if pkg.startswith("Package:"):
            output_list = pkg.split(" | ")
            cat = output_list[0].split(": ")[1].split("/")[0]
            name = output_list[0].split(": ")[1].split("/")[1].strip()
            version = output_list[1].split(": ")[1]
            newest_version = output_list[2].split(": ")[1]
            lic = output_list[3].split(": ")[1]
            hp = output_list[4].split(": ")[1]
            desc = output_list[5].split(": ")[1]

            pkg = PackageClass()
            pkg.set_data(cat, name, version, newest_version, True, lic, hp, desc)

            if cat != "virtual":
                installed.append(pkg)
                available.append(pkg)
    
    p = subprocess.Popen(["eix", "--format", '"Package: <bestversion:NAMEVERSION> | Newest: <bestversion:VERSION> | License: <licenses> | Homepage: <homepage> | Description: <description>\n"'], stdout=subprocess.PIPE, encoding="utf-8")
    out = p.stdout.readlines()

    for pkg in out:
        pkg = pkg.replace('"', "")
        if pkg.startswith("Package:") and not pkg.startswith("Package:  "):
            output_list = pkg.split(" | ")
            cat = output_list[0].split(": ")[1].split("/")[0]
            name = output_list[0].split(": ")[1].split("/")[1]
            version = output_list[1].split(": ")[1]
            newest_version = output_list[2].split(": ")[1]
            lic = output_list[3].split(": ")[1]
            hp = output_list[4].split(": ")[1]
            desc = output_list[5].split(": ")[1]

            pkg = PackageClass()
            pkg.set_data(cat, name, version, version, False, lic, hp, desc)

            if cat != "virtual":
                available.append(pkg)


class PackageClass:
    def __init__(self):
        self.category = ""
        self.pkg_name = ""
        self.pkg_version = ""
        self.best_version = ""
        self.is_installed = False
        self.license = ""
        self.homepage = ""
        self.description = ""
        self.update_available = False
    
    def get_best_version(self):
        return self.best_version

    def get_category(self):
        return self.category
    
    def get_current_version(self):
        return self.pkg_version

    def get_description(self):
        return self.description

    def get_homepage(self):
        return self.homepage
    
    def get_license(self):
        return self.license

    def get_name(self):
        return self.pkg_name

    def is_update_available(self):
        return self.update_available

    def set_data(self, cat: str, name: str, version: str, bversion: str, inst: bool, lic: str, hp: str, desc: str):
        self.category = cat
        self.pkg_name = name
        self.pkg_version = version
        self.best_version = bversion
        self.is_installed = inst
        self.license = lic
        self.homepage = hp
        self.description = desc

        if self.pkg_version == self.best_version:
            self.update_available = False
        else:
            self.update_available = True
