# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: object_detection/protos/target_assigner.proto
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
    'object_detection/protos/target_assigner.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from object_detection.protos import box_coder_pb2 as object__detection_dot_protos_dot_box__coder__pb2
from object_detection.protos import matcher_pb2 as object__detection_dot_protos_dot_matcher__pb2
from object_detection.protos import region_similarity_calculator_pb2 as object__detection_dot_protos_dot_region__similarity__calculator__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-object_detection/protos/target_assigner.proto\x12\x17object_detection.protos\x1a\'object_detection/protos/box_coder.proto\x1a%object_detection/protos/matcher.proto\x1a:object_detection/protos/region_similarity_calculator.proto\"\xcd\x01\n\x0eTargetAssigner\x12\x31\n\x07matcher\x18\x01 \x01(\x0b\x32 .object_detection.protos.Matcher\x12R\n\x15similarity_calculator\x18\x02 \x01(\x0b\x32\x33.object_detection.protos.RegionSimilarityCalculator\x12\x34\n\tbox_coder\x18\x03 \x01(\x0b\x32!.object_detection.protos.BoxCoder')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'object_detection.protos.target_assigner_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TARGETASSIGNER']._serialized_start=215
  _globals['_TARGETASSIGNER']._serialized_end=420
# @@protoc_insertion_point(module_scope)
