from nanome._internal._structure._io._mmcif.structure import structure
import nanome
import os
import tempfile
import ntpath
from nanome.api.ui import Menu
from nanome.api.ui import LayoutNode
from nanome.util.logs import Logs
from nanome.util.file import FileError

test_assets = os.getcwd() + ("/testing/test_assets")

class Icon():
    up = "test_assets/PluginIcons/Up.png"
    folder = "test_assets/PluginIcons/Folder.png"
    image = "test_assets/PluginIcons/Image.png"
    pdf = "test_assets/PluginIcons/PDF.png"
    structure = "test_assets/PluginIcons/Structures.png"
    workspace = "test_assets/PluginIcons/Workspace.png"

class FileExplorer():
    def __init__(self):
        self.item_prefab = LayoutNode.io.from_json(test_assets + "/File.json")
        self.menu = Menu.io.from_json(test_assets + "/FileExplorer.json")

        # Setup quick access panel
        self.quick_access_prefab = self.menu.root.find_node("QuickAccess1", True)
        self.file_source_node = self.quick_access_prefab.parent
        self.file_source_node.remove_child(self.quick_access_prefab)

        self.grid = self.menu.root.find_node("Grid", True).get_content()
        self.path_text = self.menu.root.find_node("BreadCrumbText", True).get_content()
        self.select_button = self.menu.root.find_node("SelectButton", True).get_content()
        self.select_button.register_pressed_callback(self.on_select_pressed)
        self.up_button = self.menu.root.find_node("Up", True).get_content()
        self.up_button.icon.value.set_all(Icon.up)
        self.up_button.register_pressed_callback(self.on_up_pressed)
        self.selected_button = None
        self.temp_dir = tempfile.mkdtemp()

    def on_up_pressed (self):
        pass

    def on_directory_pressed(self):
        pass

    def on_select_pressed(self):
        pass

    def on_quick_access(self, name):
        pass

    def set_quick_access_list (self, names):
        self.file_source_node.clear_children()
        for name in names:
            new_node = self.quick_access_prefab.clone()
            new_node.get_content().name = name
            self.file_source_node.add_child(new_node)

    def set_working_directory (self, error, path):
        self.path_text.text_value = path
        if self.running:
            self.update_content(self.path_text)

    def set_children(self, error, files):
        if error != nanome.util.FileError.no_error:  # If API couldn't access directory, display error
            nanome.util.Logs.error("Directory request error:", str(error))
            return
        self.grid.items = []
        for file in files:
            item = self.create_file_rep(file)
            if item != None:
                self.grid.items.append(item)
        if self.running:
            self.update_content(self.grid)

    def entry_pressed(self, button):
        if button.entry.is_directory:
            self.files.cd(button.entry.name, self.directory_changed)
            return
        to_update = []
        button.selected = True
        if self.selected_button is not None:
            self.selected_button.selected = False
            to_update.append(self.selected_button)
        if self.selected_button == button:
            self.selected_button = None
        else:
            self.selected_button = button
            to_update.append(self.selected_button)

        self.save_button.unusable = self.selected_button == None
        to_update.append(self.save_button)
        self.select_button.unusable = self.selected_button == None
        to_update.append(self.select_button)
        self.update_content(to_update)

    def create_file_rep(self, entry):
        extension = os.path.splitext(entry.name)[1].lower()
        icon = self.__get_icon(extension)
        if (icon == None):
            return None

        item = self.item_prefab.clone()
        button = item.find_node("Button", True).get_content()
        button.text.value.set_all(entry.name)
        button.register_pressed_callback(self.entry_pressed)
        button.entry = entry
        button.text.value.set_all(self.__path_leaf(entry.name))
        button.text.size = .3
        button.text.ellipsis = True
        button.icon.value.set_all(icon)
        return item

    def __path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def __get_icon (self, extension):
        if extension == "":
            return Icon.folder
        elif extension == ".pdf":
            return Icon.pdf
        elif extension == ".jpeg" or extension == ".jpg" or extension == ".png":
            return Icon.image
        elif extension == ".nanome":
            return Icon.workspace
#region structure formats
        elif extension == ".pdb" or extension == ".pdb1" or extension == ".pdb2" or extension == ".pdb3" or extension == ".pdb4" or extension == ".pdb5":
            return Icon.structure
        elif extension == ".sd" or extension == ".sdf" or extension == ".mol" or extension == ".mol2":
            return Icon.structure
        elif extension == ".cif" or extension == ".mmcif" or extension == ".pdbx":
            return Icon.structure
        elif extension == ".smiles" or extension == ".smi":
            return Icon.structure
        elif extension == ".xyz" or extension == ".pqr" or extension == ".gro":
            return Icon.structure
        elif extension == ".moe" or extension == ".mae" or extension == ".pse":
            return Icon.structure
#endregion
#region misc formats
        elif extension == ".dcd" or extension == ".xtc" or extension == ".trr" or extension == ".psf":
            return Icon.structure
        elif extension == ".ccp4" or extension == ".dsn6":
            return Icon.structure
        elif extension == ".dx" or extension == ".map":
            return Icon.structure
        else:
            return None
#endregion