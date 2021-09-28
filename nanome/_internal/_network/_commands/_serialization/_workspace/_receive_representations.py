from nanome._internal._util._serializers import _ArraySerializer, _TypeSerializer
from nanome._internal._shapes._serialization import _MeshSerializer

class _ReceiveRepresentations(_TypeSerializer):
    def __init__(self):
        self.array_serializer = _ArraySerializer()
        self.array_serializer.set_type(_MeshSerializer())

    def version(self):
        return 0

    def name(self):
        return "ReceiveRepresentations"

    def serialize(self, version, value, context):
        raise NotImplementedError
        #context.write_using_serializer(self.array_serializer, value)

    def deserialize(self, version, data):
        meshes = data.read_using_serializer(self.array_serializer)
        return meshes