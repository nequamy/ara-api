#!/bin/bash

PROTO_DIR="proto"
PYTHON_OUT_DIR="src"

PROTOC_DIR="protos"

echo "Generating Python code from .proto files..."

python -m grpc_tools.protoc -I$PROTO_DIR --python_out=$PYTHON_OUT_DIR/$PROTOC_DIR/ --grpc_python_out=$PYTHON_OUT_DIR/$PROTOC_DIR/ api.proto

echo "Updating imports in generated files..."

echo "Done!"