#!/bin/bash

PROTO_DIR="proto"
PYTHON_OUT_DIR="src"

DRIVER_DIR="driver"
NAV_DIR="navigation"
WEB_DIR="web"
STREAM_DIR="stream"

PROTOC_DIR="protoc"

echo "Generating Python code from .proto files..."

python -m grpc_tools.protoc -I$PROTO_DIR --python_out=$PYTHON_OUT_DIR/$STREAM_DIR/$PROTOC_DIR/ --grpc_python_out=$PYTHON_OUT_DIR/$STREAM_DIR/$PROTOC_DIR/ $PROTO_DIR/stream.proto
python -m grpc_tools.protoc -I$PROTO_DIR --python_out=$PYTHON_OUT_DIR/$DRIVER_DIR/$PROTOC_DIR/ --grpc_python_out=$PYTHON_OUT_DIR/$DRIVER_DIR/$PROTOC_DIR/ $PROTO_DIR/driver.proto
python -m grpc_tools.protoc -I$PROTO_DIR --python_out=$PYTHON_OUT_DIR/$NAV_DIR/$PROTOC_DIR/ --grpc_python_out=$PYTHON_OUT_DIR/$NAV_DIR/$PROTOC_DIR/ $PROTO_DIR/navigation.proto
python -m grpc_tools.protoc -I$PROTO_DIR --python_out=$PYTHON_OUT_DIR/$WEB_DIR/$PROTOC_DIR/ --grpc_python_out=$PYTHON_OUT_DIR/$WEB_DIR/$PROTOC_DIR/ $PROTO_DIR/web.proto

echo "Updating imports in generated files..."

for file in $PYTHON_OUT_DIR/$DRIVER_DIR/$PROTOC_DIR/driver_pb2_grpc.py; do
    sed -i 's/import \([a-z_]*\)_pb2/from \1.protoc import \1_pb2/g' "$file"
done

for file in $PYTHON_OUT_DIR/$NAV_DIR/$PROTOC_DIR/navigation_pb2_grpc.py; do
    sed -i 's/import \([a-z_]*\)_pb2/from \1.protoc import \1_pb2/g' "$file"
done

for file in $PYTHON_OUT_DIR/$WEB_DIR/$PROTOC_DIR/web_pb2_grpc.py; do
    sed -i 's/import \([a-z_]*\)_pb2/from \1.protoc import \1_pb2/g' "$file"
done

for file in $PYTHON_OUT_DIR/$STREAM_DIR/$PROTOC_DIR/stream_pb2_grpc.py; do
    sed -i 's/import \([a-z_]*\)_pb2/from \1.protoc import \1_pb2/g' "$file"
done

echo "Done!"