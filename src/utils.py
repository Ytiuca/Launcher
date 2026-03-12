import os
from gi.repository import GLib


def get_data_path() -> str:
    data_dir = GLib.get_user_data_dir()

    app_dir = os.path.join(data_dir, "com.acuity.Launcher")
    os.makedirs(app_dir, exist_ok=True)

    return os.path.join(app_dir, "user_projects.json")
