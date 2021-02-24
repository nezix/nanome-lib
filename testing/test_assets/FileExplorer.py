import nanome
from nanome.api.ui import Menu
from nanome.api.ui import LayoutNode
import os
import tempfile
import ntpath

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

    def on_up_pressed(self):
        pass

    def on_directory_pressed(self, entry):
        pass

    def on_select_pressed(self, entry):
        pass

    def on_quick_access(self, name):
        pass

    def set_quick_access_list(self, names):
        self.file_source_node.clear_children()
        for name in names:
            new_node = self.quick_access_prefab.clone()
            button = new_node.get_content()
            button.name = name
            button.text.value.set_all(name)
            button.register_pressed_callback(self.__quick_access_pressed)
            self.file_source_node.add_child(new_node)

    def set_working_directory(self, error, path):
        self.path_text.text_value = path

    def set_directory_contents(self, error, files):
        if error != nanome.util.FileError.no_error:  # If API couldn't access directory, display error
            nanome.util.Logs.error("Directory request error:", str(error))
            return
        self.grid.items = []
        for file in files:
            item = self.__create_file_rep(file)
            if item != None:
                self.grid.items.append(item)

    def __quick_access_pressed(self, button):
        self.on_quick_access(button.name)

    def __entry_pressed(self, button):
        to_update = []
        # deselecting a node
        if self.selected_button == button:
            self.selected_button = None
            button.selected = False
            to_update.append(button)
            self.select_button.unusable = True
            to_update.append(self.select_button)
        # selecting a node
        else:
            #deselecting the old node
            if self.selected_button is not None:
                self.selected_button.selected = False
                to_update.append(self.selected_button)
            else:
                self.select_button.unusable = False
                to_update.append(self.select_button)
            button.selected = True
            to_update.append(button)
            self.selected_button = button
        # self.update_content(to_update)

    def __directory_pressed(self, button):
        self.on_directory_pressed(button.entry)

    def __get_prefab_parts(self, prefab):
        selection_button = prefab.find_node("Selection", True).get_content()
        icon = prefab.find_node("Icon", True).get_content()
        text = prefab.find_node("Name", True).get_content()

        favorite_node = prefab.find_node("Favorite", True)
        favorite_button = favorite_node.get_content()

        date_and_size_node = prefab.find_node("DateAndSize", True).get_content()
        date = prefab.find_node("Date", True).get_content()
        size = prefab.find_node("Size", True).get_content()
        return selection_button, icon, text, favorite_node, favorite_button, date_and_size_node, date, size

    def __create_file_rep(self, entry):
        extension = os.path.splitext(entry.name)[1].lower()
        image = self.__get_icon(extension)
        if (image == None):
            return None

        item = self.item_prefab.clone()
        selection_button, icon, text, favorite_node, favorite_button, date_and_size_node, date, size = self.__get_prefab_parts(item)

        selection_button.entry = entry

        icon.icon.value.set_all(image)
        text.text_value.set_all(self.__path_leaf(entry.name))

        if entry.is_directory:
            selection_button.register_pressed_callback(self.__directory_pressed)
            # favorite_node.enabled(True) #Disabling favorite behaviour for now
            date_and_size_node.enabled(False)
        else:
            selection_button.register_pressed_callback(self.__entry_pressed)
            # favorite_node.enabled(False)
            date_and_size_node.enabled(True)
            date.text_value.set_all(entry.date_modified)
            size.text_value.set_all(entry.size)
        return item

    def __path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def __get_icon(self, extension):
        if extension == "":
            return Icon.folder
        elif extension == ".pdf":
            return Icon.pdf
        elif extension == ".jpeg" or extension == ".jpg" or extension == ".png":
            return Icon.image
        elif extension == ".nanome":
            return Icon.workspace
# region structure formats
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
# endregion
# region misc formats
        elif extension == ".dcd" or extension == ".xtc" or extension == ".trr" or extension == ".psf":
            return Icon.structure
        elif extension == ".ccp4" or extension == ".dsn6":
            return Icon.structure
        elif extension == ".dx" or extension == ".map":
            return Icon.structure
        else:
            return None
# endregion
