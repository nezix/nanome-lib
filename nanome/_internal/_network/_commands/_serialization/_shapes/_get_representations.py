from nanome._internal._util._serializers import _ArraySerializer, _LongSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _RequestRepresentations(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestRepresentations"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None
