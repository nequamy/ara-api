# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: api.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'api.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tapi.proto\"\x1a\n\x0b\x43ommandData\x12\x0b\n\x03\x63md\x18\x01 \x01(\t\"#\n\x0f\x41ltitudeSetData\x12\x10\n\x08\x61ltitude\x18\x01 \x01(\x02\"\x1c\n\nStatusData\x12\x0e\n\x06status\x18\x01 \x01(\t\"$\n\tPointData\x12\x17\n\x05point\x18\x01 \x01(\x0b\x32\x08.Vector3\"*\n\x0cVelocityData\x12\x1a\n\x08velocity\x18\x01 \x01(\x0b\x32\x08.Vector3\" \n\x0cSettingsData\x12\x10\n\x08settings\x18\x01 \x01(\t\"|\n\nRcDataData\x12\x0b\n\x03\x61il\x18\x01 \x01(\r\x12\x0b\n\x03\x65le\x18\x02 \x01(\r\x12\x0b\n\x03thr\x18\x03 \x01(\r\x12\x0b\n\x03rud\x18\x04 \x01(\r\x12\r\n\x05\x61ux_1\x18\x05 \x01(\r\x12\r\n\x05\x61ux_2\x18\x06 \x01(\r\x12\r\n\x05\x61ux_3\x18\x07 \x01(\r\x12\r\n\x05\x61ux_4\x18\x08 \x01(\r\"L\n\tFlagsData\x12\x15\n\ractiveSensors\x18\x01 \x01(\t\x12\x1a\n\x12\x61rmingDisableFlags\x18\x02 \x01(\t\x12\x0c\n\x04mode\x18\x03 \x01(\t\"O\n\tMotorData\x12\x0f\n\x07motor_1\x18\x01 \x01(\x05\x12\x0f\n\x07motor_2\x18\x02 \x01(\x05\x12\x0f\n\x07motor_3\x18\x03 \x01(\x05\x12\x0f\n\x07motor_4\x18\x04 \x01(\x05\"8\n\x07IMUData\x12\x16\n\x04gyro\x18\x01 \x01(\x0b\x32\x08.Vector3\x12\x15\n\x03\x61\x63\x63\x18\x02 \x01(\x0b\x32\x08.Vector3\"(\n\x0c\x41ttitudeData\x12\x18\n\x06orient\x18\x01 \x01(\x0b\x32\x08.Vector3\" \n\x0c\x41ltitudeData\x12\x10\n\x08\x61ltitude\x18\x01 \x01(\x02\"\x1a\n\tSonarData\x12\r\n\x05sonar\x18\x01 \x01(\x02\"v\n\x0fOpticalFlowData\x12\x0f\n\x07quality\x18\x01 \x01(\x05\x12\x13\n\x0b\x66low_rate_x\x18\x02 \x01(\x02\x12\x13\n\x0b\x66low_rate_y\x18\x03 \x01(\x02\x12\x13\n\x0b\x62ody_rate_x\x18\x04 \x01(\x02\x12\x13\n\x0b\x62ody_rate_y\x18\x05 \x01(\x02\"%\n\x0cOdometryData\x12\x15\n\x03pos\x18\x01 \x01(\x0b\x32\x08.Vector3\"O\n\nAnalogData\x12\x0f\n\x07voltage\x18\x01 \x01(\x02\x12\x10\n\x08mAhdrawn\x18\x02 \x01(\x05\x12\x0c\n\x04rssi\x18\x03 \x01(\x05\x12\x10\n\x08\x61mperage\x18\x04 \x01(\x02\"\x19\n\nGetRequest\x12\x0b\n\x03req\x18\x01 \x01(\t\"*\n\x07Vector3\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x32\x84\x03\n\rDriverManager\x12&\n\rGetImuDataRPC\x12\x0b.GetRequest\x1a\x08.IMUData\x12*\n\x0fGetSonarDataRPC\x12\x0b.GetRequest\x1a\n.SonarData\x12,\n\x10GetAnalogDataRPC\x12\x0b.GetRequest\x1a\x0b.AnalogData\x12\x30\n\x12GetAttitudeDataRPC\x12\x0b.GetRequest\x1a\r.AttitudeData\x12\x30\n\x12GetOdometryDataRPC\x12\x0b.GetRequest\x1a\r.OdometryData\x12\x36\n\x15GetOpticalFlowDataRPC\x12\x0b.GetRequest\x1a\x10.OpticalFlowData\x12*\n\x0fGetFlagsDataRPC\x12\x0b.GetRequest\x1a\n.FlagsData\x12)\n\rSendRcDataRPC\x12\x0b.RcDataData\x1a\x0b.StatusData2\xdb\x01\n\x11NavigationManager\x12(\n\x07TakeOFF\x12\x10.AltitudeSetData\x1a\x0b.StatusData\x12%\n\x04Land\x12\x10.AltitudeSetData\x1a\x0b.StatusData\x12\x1f\n\x04Move\x12\n.PointData\x1a\x0b.StatusData\x12)\n\x0bSetVelocity\x12\r.VelocityData\x1a\x0b.StatusData\x12)\n\x0bSetSettings\x12\r.SettingsData\x1a\x0b.StatusDatab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_COMMANDDATA']._serialized_start=13
  _globals['_COMMANDDATA']._serialized_end=39
  _globals['_ALTITUDESETDATA']._serialized_start=41
  _globals['_ALTITUDESETDATA']._serialized_end=76
  _globals['_STATUSDATA']._serialized_start=78
  _globals['_STATUSDATA']._serialized_end=106
  _globals['_POINTDATA']._serialized_start=108
  _globals['_POINTDATA']._serialized_end=144
  _globals['_VELOCITYDATA']._serialized_start=146
  _globals['_VELOCITYDATA']._serialized_end=188
  _globals['_SETTINGSDATA']._serialized_start=190
  _globals['_SETTINGSDATA']._serialized_end=222
  _globals['_RCDATADATA']._serialized_start=224
  _globals['_RCDATADATA']._serialized_end=348
  _globals['_FLAGSDATA']._serialized_start=350
  _globals['_FLAGSDATA']._serialized_end=426
  _globals['_MOTORDATA']._serialized_start=428
  _globals['_MOTORDATA']._serialized_end=507
  _globals['_IMUDATA']._serialized_start=509
  _globals['_IMUDATA']._serialized_end=565
  _globals['_ATTITUDEDATA']._serialized_start=567
  _globals['_ATTITUDEDATA']._serialized_end=607
  _globals['_ALTITUDEDATA']._serialized_start=609
  _globals['_ALTITUDEDATA']._serialized_end=641
  _globals['_SONARDATA']._serialized_start=643
  _globals['_SONARDATA']._serialized_end=669
  _globals['_OPTICALFLOWDATA']._serialized_start=671
  _globals['_OPTICALFLOWDATA']._serialized_end=789
  _globals['_ODOMETRYDATA']._serialized_start=791
  _globals['_ODOMETRYDATA']._serialized_end=828
  _globals['_ANALOGDATA']._serialized_start=830
  _globals['_ANALOGDATA']._serialized_end=909
  _globals['_GETREQUEST']._serialized_start=911
  _globals['_GETREQUEST']._serialized_end=936
  _globals['_VECTOR3']._serialized_start=938
  _globals['_VECTOR3']._serialized_end=980
  _globals['_DRIVERMANAGER']._serialized_start=983
  _globals['_DRIVERMANAGER']._serialized_end=1371
  _globals['_NAVIGATIONMANAGER']._serialized_start=1374
  _globals['_NAVIGATIONMANAGER']._serialized_end=1593
# @@protoc_insertion_point(module_scope)
