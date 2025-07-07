def create_index_if_not_exists(client, index_name: str):
    if not client.indices.exists(index=index_name):
        mapping = {
            "mappings": {
                "properties": {
                    "timestamp": {"type": "date"},
                    "level": {"type": "keyword"},
                    "message": {"type": "text"},
                    "service": {"type": "keyword"},
                }
            }
        }
        client.indices.create(index=index_name, body=mapping)
