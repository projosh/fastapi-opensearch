import os
from opensearchpy import OpenSearch

def get_client():
    host = os.getenv("OPENSEARCH_HOST", "localhost")
    port = int(os.getenv("OPENSEARCH_PORT", 9200))
    return OpenSearch([{"host": host, "port": port}])
