import os
import platform
import sys

from PyQt6.QtWidgets import (
    QMainWindow,
    QInputDialog,
    QDockWidget,
    QTreeView,
    QFileDialog,
    QSplashScreen,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QStatusBar,
    QListWidget,
    QLabel,
    QDialog)
from PyQt6.QtGui import QFont
import pathspec

from auratext.Misc.import_res import notepadequalequalComponentImportPathAppend
sys.path.append(notepadequalequalComponentImportPathAppend)
from notepadequalequal.fileio import retrieve_file

if platform.system() == "Windows":
    local_app_data = os.getenv('LOCALAPPDATA')
elif platform.system() == "Linux":
    local_app_data = os.path.expanduser("~/.config")
elif platform.system() == "Darwin":
    local_app_data = os.path.expanduser("~/Library/Application Support")
else:
    print("Unsupported operating system")
    sys.exit(1)

local_app_data = os.path.join(local_app_data, "AuraText")
script_dir = os.path.dirname(os.path.abspath(__file__))

class BoilerPlate(QDialog):
    def __init__(self, current_editor):
        super().__init__()
        self.setWindowTitle("Boilerplates")

        self.current_editor = current_editor

        # Create a layout for the dock widget
        dock_layout = QVBoxLayout()
        self.setLayout(dock_layout)
        # self.boilerplate_dock.setLayout(dock_layout)

        # Add a header label to the dock widget
        header_label = QLabel("Boilerplates")
        header_label.setStyleSheet("QLabel{font-size: 20px; font : Arial;}")
        dock_layout.addWidget(header_label)

        # Create a QListWidget for displaying file names
        self.boilerplate_list = QListWidget()
        dock_layout.addWidget(self.boilerplate_list)

        # Populate the QListWidget with file names
        directory = f"{local_app_data}/boilerplates"
        if os.path.exists(directory):
            try:
                for file_name in os.listdir(directory):
                    if os.path.isfile(os.path.join(directory, file_name)):
                        name, extension = os.path.splitext(file_name)
                        self.boilerplate_list.addItem(name)
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"The directory '{directory}' does not exist.")

            # Connect the clicked signal to a custom slot method
            self.boilerplate_list.clicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item):
        print("Function reached")
        selected_file = item.text()

        # Read the contents of the selected file
        file_path = os.path.join(local_app_data, "boilerplates", f"{selected_file}.txt")
        try:
            file_contents = retrieve_file(file_path)
            print(file_contents)
            self.current_editor.append(file_contents)
        except Exception as e:
            print(f"Error reading file: {e}")

def get_font_for_platform(size=12, plain=True):
    system_name = platform.system()
    if system_name == "Windows":
        if plain == True:
            return QFont("Consolas", size)
        else:
            return QFont("Arial", size)
    elif system_name == "Darwin":
        if plain:
            return QFont("Menlo", size)
        else:
            return QFont("Helvetica", size)
    else:
        if plain:
            return QFont("DejaVu Sans Mono", size)
        else:
            return QFont("Noto Sans", size)
        
def pathspec_gitignore_parse(gitignore_path):
    with open(gitignore_path, "r") as f:
        lines = f.read().splitlines()
        
    spec = pathspec.PathSpec.from_lines('gitwildmatch', lines)
    
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]

def is_under_parent_dir(path, parent_dir):
    path = os.path.abspath(path)
    parent_dir = os.path.abspath(parent_dir)
    return os.path.commonpath([path, parent_dir]) == parent_dir

def is_under_parent_list(path, parent_dirs):
    n = 0
    for parent_dir in parent_dirs:
        if is_under_parent_dir(path, parent_dir):
            n += 1
    if n > 0:
        return True
    else:
        return False

def get_appdata_dirs():
    if platform.system() == "Windows":
        local_app_data = os.getenv('LOCALAPPDATA')
    elif platform.system() == "Linux":
        local_app_data = os.path.expanduser("~/.config")
    elif platform.system() == "Darwin":
        local_app_data = os.path.expanduser("~/Library/Application Support")
    else:
        print("Unsupported operating system")
        sys.exit(1)

    local_app_data = os.path.join(local_app_data, "AuraText")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    return local_app_data, script_dir
