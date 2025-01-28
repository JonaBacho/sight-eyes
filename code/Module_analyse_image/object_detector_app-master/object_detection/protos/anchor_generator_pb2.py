# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: object_detection/protos/anchor_generator.proto
# Protobuf Python Version: 5.28.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    3,
    '',
    'object_detection/protos/anchor_generator.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from object_detection.protos import flexible_grid_anchor_generator_pb2 as object__detection_dot_protos_dot_flexible__grid__anchor__generator__pb2
from object_detection.protos import grid_anchor_generator_pb2 as object__detection_dot_protos_dot_grid__anchor__generator__pb2
from object_detection.protos import multiscale_anchor_generator_pb2 as object__detection_dot_protos_dot_multiscale__anchor__generator__pb2
from object_detection.protos import ssd_anchor_generator_pb2 as object__detection_dot_protos_dot_ssd__anchor__generator__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.object_detection/protos/anchor_generator.proto\x12\x17object_detection.protos\x1a<object_detection/protos/flexible_grid_anchor_generator.proto\x1a\x33object_detection/protos/grid_anchor_generator.proto\x1a\x39object_detection/protos/multiscale_anchor_generator.proto\x1a\x32object_detection/protos/ssd_anchor_generator.proto\"\x82\x03\n\x0f\x41nchorGenerator\x12M\n\x15grid_anchor_generator\x18\x01 \x01(\x0b\x32,.object_detection.protos.GridAnchorGeneratorH\x00\x12K\n\x14ssd_anchor_generator\x18\x02 \x01(\x0b\x32+.object_detection.protos.SsdAnchorGeneratorH\x00\x12Y\n\x1bmultiscale_anchor_generator\x18\x03 \x01(\x0b\x32\x32.object_detection.protos.MultiscaleAnchorGeneratorH\x00\x12^\n\x1e\x66lexible_grid_anchor_generator\x18\x04 \x01(\x0b\x32\x34.object_detection.protos.FlexibleGridAnchorGeneratorH\x00\x42\x18\n\x16\x61nchor_generator_oneof')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'object_detection.protos.anchor_generator_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANCHORGENERATOR']._serialized_start=302
  _globals['_ANCHORGENERATOR']._serialized_end=688
# @@protoc_insertion_point(module_scope)
