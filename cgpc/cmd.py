#!/usr/bin/env python3

import subprocess


def get_app_information(category: str, name: str):
    search_name = category + "/" + name

    if search_name in get_installed_list():
        p = subprocess.Popen(["eix", "-IC", category, name, "--format", '"Package: <installedversions:NAMEVERSION> | License: <licenses> | Homepage: <homepage> | Description: <description>\n"'], stdout=subprocess.PIPE, encoding="utf-8")
    else:
        p = subprocess.Popen(["eix", "-C", category, name + "$", "--format", '"Package: <bestversion:NAMEVERSION> | License: <licenses> | Homepage: <homepage> | Description: <description>\n"'], stdout=subprocess.PIPE, encoding="utf-8")

    out = p.stdout.readlines()

    return out


def get_installed_list():
    p = subprocess.Popen(["eix", "-I#"], stdout=subprocess.PIPE, encoding="utf-8")
    installed = list(p.stdout.read().split())
    return installed


def get_pkg_best_version(category: str, name: str):
    search_name = category + "/" + name

    if search_name in get_installed_list():
        arg = "-IC"
    else:
        arg = "-C"

    if name[-1].isalpha():
        p = subprocess.Popen(["eix", arg, category, name + "$", "--format", '"Package: <bestversion:NAMEVERSION>\n"'], stdout=subprocess.PIPE, encoding="utf-8")
    else:
        p = subprocess.Popen(["eix", arg, category, name, "--format", '"Package: <bestversion:NAMEVERSION>\n"'], stdout=subprocess.PIPE, encoding="utf-8")

    out = p.stdout.readlines()
    return out


def get_updates_list():
    p = subprocess.Popen(["eix", "-u#"], stdout=subprocess.PIPE, encoding="utf-8")

    out = p.stdout.read().split()

    return out
