#defines a single leg
from nanome.util import Logs
import testing
class FuzzerCommand(object):
    def __init__(self, fuzzer_info, plugin):
        self.done = False
        self.fuzzer_info = fuzzer_info
        self.plugin = plugin
        Logs.message("Selected Command:", self.get_name())
        Logs.inc_tab()
        self.define_callbacks()

    def define_callbacks(self):
        self._on_complex_received = lambda *args: None

    def finish(self, *args):
        self.done = True
        Logs.dec_tab()
        Logs.message("Finished Command:", self.get_name())

    #region interface
    def _get_name(self):
        raise NotImplementedError()

    def _rules(self, FuzzerInfo):
        raise NotImplementedError()

    def _run(self, FuzzerInfo):
        raise NotImplementedError()
    #endregion

    #region external API
    def get_name(self):
        return self._get_name()
    
    def get_done(self):
        return self.done

    def rules(self):
        Logs.message("Checking rules...")
        Logs.inc_tab()
        success = self._rules()
        if not success:
            Logs.message("failed")
        else:
            Logs.message("success")
        Logs.dec_tab()
        return success

    def run(self):
        Logs.message("Running...")
        Logs.inc_tab()
        result = self._run()
        return result
    #endregion

    #region helpers
    def get_random_complex(self, callback):
        self.plugin.request_workspace(self.__get_random_complex)
        self._on_complex_received = callback

    def get_random_conformer(self, callback):

    def get_random_molecule(self, callback):

    def get_workspace(self, callback):
        self.plugin.request_workspace(callback)

    def update_structures(self, structures, callback):
        if not isinstance(structures, list):
            structures = list(structures)
        self.plugin.update_structures_deep(structures, callback)

    def has_conformer (self, complex, default = False):
        all_mol = list(complex.molecules)
        if len(all_mol) > 1:
            return False
        mol = all_mol[0]
        if mol.conformer_count > 1:
            return True
        #default
        return default

    #endregion helpers

    def __get_random_complex(self, workspace):
        complexes = workspace.complexes
        r_c = testing.rand_index(complexes)
        complex = workspace.complexes[r_c]
        self._on_complex_received(complex)

class ExampleCommand(FuzzerCommand):
    def __init__(self):
        FuzzerCommand.__init__(self)
        self.done = False

    def _get_name(self):
        return "Example"

    def _rules(self, FuzzerInfo):
        return True

    def _run(self, FuzzerInfo):
        pass