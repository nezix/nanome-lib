from nanome._internal._util._serializers import _ArraySerializer, _LongSerializer, _TypeSerializer
from nanome._internal._shapes._serialization import _MeshSerializer


class _RequestRepresentations(_TypeSerializer):
    def __init__(self):
        self.array_serializer = _ArraySerializer()
        self.array_serializer.set_type(_MeshSerializer())
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestRepresentations"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None