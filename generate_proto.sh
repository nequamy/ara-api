#!/bin/bash

PROTO_DIR="proto"

echo "Generating Python code from .proto files..."

python -m grpc_tools.protoc -I$PROTO_DIR --python_out=src/stream/protoc      --grpc_python_out=src/stream/protoc         $PROTO_DIR/stream.proto
python -m grpc_tools.protoc -I$PROTO_DIR --python_out=src/driver/protoc      --grpc_python_out=src/driver/protoc         $PROTO_DIR/driver.proto
python -m grpc_tools.protoc -I$PROTO_DIR --python_out=src/navigation/protoc  --grpc_python_out=src/navigation/protoc     $PROTO_DIR/navigation.proto
python -m grpc_tools.protoc -I$PROTO_DIR --python_out=src/web/protoc         --grpc_python_out=src/web/protoc            $PROTO_DIR/web.proto

echo "Done!"