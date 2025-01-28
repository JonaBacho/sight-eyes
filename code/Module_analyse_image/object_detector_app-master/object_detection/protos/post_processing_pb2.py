# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: object_detection/protos/post_processing.proto
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
    'object_detection/protos/post_processing.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from object_detection.protos import calibration_pb2 as object__detection_dot_protos_dot_calibration__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-object_detection/protos/post_processing.proto\x12\x17object_detection.protos\x1a)object_detection/protos/calibration.proto\"\xc9\x03\n\x16\x42\x61tchNonMaxSuppression\x12\x1a\n\x0fscore_threshold\x18\x01 \x01(\x02:\x01\x30\x12\x1a\n\riou_threshold\x18\x02 \x01(\x02:\x03\x30.6\x12%\n\x18max_detections_per_class\x18\x03 \x01(\x05:\x03\x31\x30\x30\x12!\n\x14max_total_detections\x18\x05 \x01(\x05:\x03\x31\x30\x30\x12 \n\x11use_static_shapes\x18\x06 \x01(\x08:\x05\x66\x61lse\x12%\n\x16use_class_agnostic_nms\x18\x07 \x01(\x08:\x05\x66\x61lse\x12$\n\x19max_classes_per_detection\x18\x08 \x01(\x05:\x01\x31\x12\x19\n\x0esoft_nms_sigma\x18\t \x01(\x02:\x01\x30\x12\"\n\x13use_partitioned_nms\x18\n \x01(\x08:\x05\x66\x61lse\x12\x1f\n\x10use_combined_nms\x18\x0b \x01(\x08:\x05\x66\x61lse\x12%\n\x17\x63hange_coordinate_frame\x18\x0c \x01(\x08:\x04true\x12\x1b\n\x0cuse_hard_nms\x18\r \x01(\x08:\x05\x66\x61lse\x12\x1a\n\x0buse_cpu_nms\x18\x0e \x01(\x08:\x05\x66\x61lse\"\xd9\x02\n\x0ePostProcessing\x12R\n\x19\x62\x61tch_non_max_suppression\x18\x01 \x01(\x0b\x32/.object_detection.protos.BatchNonMaxSuppression\x12Y\n\x0fscore_converter\x18\x02 \x01(\x0e\x32\x36.object_detection.protos.PostProcessing.ScoreConverter:\x08IDENTITY\x12\x16\n\x0blogit_scale\x18\x03 \x01(\x02:\x01\x31\x12\x46\n\x12\x63\x61libration_config\x18\x04 \x01(\x0b\x32*.object_detection.protos.CalibrationConfig\"8\n\x0eScoreConverter\x12\x0c\n\x08IDENTITY\x10\x00\x12\x0b\n\x07SIGMOID\x10\x01\x12\x0b\n\x07SOFTMAX\x10\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'object_detection.protos.post_processing_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_BATCHNONMAXSUPPRESSION']._serialized_start=118
  _globals['_BATCHNONMAXSUPPRESSION']._serialized_end=575
  _globals['_POSTPROCESSING']._serialized_start=578
  _globals['_POSTPROCESSING']._serialized_end=923
  _globals['_POSTPROCESSING_SCORECONVERTER']._serialized_start=867
  _globals['_POSTPROCESSING_SCORECONVERTER']._serialized_end=923
# @@protoc_insertion_point(module_scope)
