from . import _DefaultPlugin
from nanome._internal import _Plugin
from nanome._internal._process import _ProcessManager
from nanome.util.logs import Logs
from nanome.util import config


class Plugin(_Plugin):
    """
    | Core class of any Plugin.
    | Manages network, callbacks and APIs

    :param name: Name of the plugin to display
    :param description: Description of the plugin to display
    :param category: Category of the plugin
    :param has_advanced: If true, plugin will display an "Advanced Settings" button
    :type name: str
    :type description: str
    :type category: str
    :type has_advanced: bool
    """
    @classmethod
    def setup(cls, name, description, category, has_advanced, plugin_class, host="config", port="config", key_file="config"):
        if not _Plugin._is_process():
            plugin = cls(name, description, category, has_advanced)
            plugin.set_plugin_class(plugin_class)
            plugin.run(host, port, key_file)

    @staticmethod
    def set_custom_data(*args):
        """
        | Store arbitrary data to send to plugin instances

        :param args: Variable length argument list
        :type args: Anything serializable
        """
        _Plugin._custom_data = args

    @staticmethod
    def set_maximum_processes_count(max_process_nb):
        _ProcessManager._max_process_count = max_process_nb

    def run(self, host="config", port="config", key_file="config"):
        """
        | Starts the plugin by connecting to the server specified.
        | If arguments (-a, -p) are given when starting plugin, host/port will be ignored.
        | Function will return only when plugin exits.

        :param host: NTS IP address if plugin started without -a option
        :param port: NTS port if plugin started without -p option
        :type host: str
        :type port: int
        """
        if (host == "config"):
            self.__host = config.fetch("host")
        else:
            self.__host = host
        if (port == "config"):
            self.__port = config.fetch("port")
        else:
            self.__port = port
        if (key_file == "config"):
            self.__key_file = config.fetch("key_file")
        else:
            self.__key_file = key_file
        self.__parse_args()
        Logs.debug("Start plugin")
        if self.__has_autoreload:
            self.__autoreload()
        else:
            self.__run()

    def set_plugin_class(self, plugin_class):
        """
        | Set plugin class to instantiate when a new session is connected
        | The plugin class should interact with or override functions in :class:`~nanome.api.plugin_instance.PluginInstance` to interact with Nanome

        :param plugin_class: Plugin class to instantiate
        :type plugin_class: :class:`~nanome.api.plugin_instance.PluginInstance`
        """
        self._plugin_class = plugin_class

    @property
    def pre_run(self):
        """
        | Function to call before the plugin runs and tries to connect to NTS
        | Useful when using autoreload
        """
        return self._pre_run

    @pre_run.setter
    def pre_run(self, value):
        self._pre_run = value

    @property
    def post_run(self):
        """
        | Function to call when the plugin is about to exit
        | Useful when using autoreload
        """
        return self._post_run

    @post_run.setter
    def post_run(self, value):
        self._post_run = value

    @property
    def autoreload(self):
        """
        | Boolean determining whether the server reloads on save.
        """
        return self.__autoreload

    @autoreload.setter
    def autoreload(self, value):
        self.__autoreload = value

    def __init__(self, name, description, category="", has_advanced=False):
        super(Plugin, self).__init__(name, description, category, has_advanced)
        self._plugin_class = _DefaultPlugin
