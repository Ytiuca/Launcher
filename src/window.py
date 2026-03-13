# window.py
#
# Copyright 2026 Acuity
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw
import subprocess
import json
import os
from .project import Project
from .utils import get_data_path


@Gtk.Template(resource_path="/com/acuity/Launcher/window.ui")
class LauncherWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "LauncherWindow"

    container = Gtk.Template.Child()
    search_bar = Gtk.Template.Child()
    add_project = Gtk.Template.Child()
    projects: list[Project] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.projects = self.load_projects()
        self.add_project.connect("clicked", self.on_add_project)
        self.search_bar.connect("changed", self.on_search)
        self.display_projects(self.projects)

    def load_projects(self):
        data_path = get_data_path()
        if not os.path.exists(data_path):
            with open(data_path, "w") as f:
                f.write("{}")

        with open(data_path, "r") as f:
            data = json.load(f)
        return [Project(**item) for item in data]

    def on_add_project(self, button: Gtk.Button):
        project = Project("", "")
        self.projects.append(project)
        self.display_projects(self.projects)
        self.on_edit()

    def on_search(self, entry: Gtk.Entry):
        search_input = entry.get_text().lower()
        self.display_projects(
            list(filter(lambda p: search_input in p.name.lower(), self.projects))
        )

    def on_start_project(self, command_entry: Gtk.Entry):
        executed_command = (
            (
                "flatpak-spawn --host "
                if os.environ.get("FLATPAK_ID") is not None
                else ""
            )
            + command_entry.get_text()
        ).split(" ")
        print(f"{executed_command=}")
        error = ""
        try:
            subprocess.Popen(executed_command, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            # ça c'est les exceptions au lancement de la commande
            error = str(e)

        if error != "":
            self.show_error_dialog(error)

    def show_error_dialog(self, error):
        dialog = Adw.MessageDialog(transient_for=self, heading="Error", body=error)
        dialog.add_response("close", "Close")
        dialog.present()

    def on_update_project(
        self, project: Project, entry_name: Gtk.Entry, entry_command: Gtk.Entry
    ):
        project.name = entry_name.get_text()
        project.command = entry_command.get_text()
        self.on_edit()

    def display_projects(self, projects: list[Project]):
        # Boucle efficace : on retire le premier enfant jusqu'à ce qu'il n'y en ait plus
        while child := self.container.get_first_child():
            self.container.remove(child)
        for project in projects:
            une_ligne = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            une_ligne.set_margin_bottom(10)
            une_ligne.set_margin_start(10)
            une_ligne.set_margin_end(10)

            entry_project = Gtk.Entry()
            entry_project.set_hexpand(True)
            entry_project.set_text(project.name)
            entry_project.set_sensitive(False)
            une_ligne.append(entry_project)

            entry_command = Gtk.Entry()
            entry_command.set_hexpand(True)
            entry_command.set_text(project.command)
            entry_command.set_visible(False)
            une_ligne.append(entry_command)

            entry_project.connect(
                "changed",
                lambda entry, entry_command=entry_command: self.on_update_project(
                    project, entry, entry_command
                ),
            )
            entry_command.connect(
                "changed",
                lambda entry, entry_project=entry_project: self.on_update_project(
                    project, entry_project, entry
                ),
            )

            button_start = Gtk.Button(icon_name="media-playback-start-symbolic")
            button_start.connect(
                "clicked",
                lambda button, entry_command=entry_command: self.on_start_project(
                    entry_command
                ),
            )
            une_ligne.append(button_start)

            button_edit = Gtk.Button(icon_name="document-edit-symbolic")
            button_edit.connect(
                "clicked",
                lambda button, entry_command=entry_command, entry_project=entry_project: entry_command.set_visible(
                    not entry_command.get_visible()
                )
                or entry_project.set_sensitive(not entry_project.get_sensitive()),
            )
            une_ligne.append(button_edit)

            button_delete = Gtk.Button(icon_name="user-trash-symbolic")
            button_delete.connect(
                "clicked",
                lambda button: self.projects.remove(project)
                or self.display_projects(self.projects)
                or self.on_edit(),
            )
            une_ligne.append(button_delete)

            self.container.append(une_ligne)

    def on_edit(self):
        self.set_title("Launcher*")
