import nanome
from nanome._internal._network import PluginNetwork
from nanome._internal._network._commands._callbacks import _Messages


class _Room():
    SkyBoxes = nanome.util.enums.SkyBoxes

    def __init__(self):
        pass

    def _set_skybox(self, skybox):
        PluginNetwork._send(_Messages.set_skybox, skybox, False)
