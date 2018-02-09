all:
	protoc --python_out=. --proto_path=. gossip.proto
