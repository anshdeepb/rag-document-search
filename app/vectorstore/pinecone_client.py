import os
from pinecone import Pinecone
from dotenv import load_dotenv
import time

load_dotenv()

environment = 'us-east-1'
INDEX_NAME = "rag-pipeline-pdf-response"


#configure client

def initialize_db(api_key):
    pc = Pinecone(api_key=api_key)

    from pinecone import ServerlessSpec

    cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
    region = os.environ.get('PINECONE_REGION') or 'us-east-1'

    spec = ServerlessSpec(cloud=cloud, region=region)
    index = create_index(pc, spec)

    return index

def create_index(pc, spec):

    index_name = INDEX_NAME
    existing_indexes = [
    index_info["name"] for index_info in pc.list_indexes()
]

    if index_name not in existing_indexes:

        pc.create_index(
        index_name,
        dimension=1536, 
        metric='cosine',
        spec=spec
    )

        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)


    index = pc.Index(index_name)
    time.sleep(1)

    index.describe_index_stats()
    return index

def connect_to_existing_index(api_key):
    pc = Pinecone(api_key=api_key)

    existing = [info["name"] for info in pc.list_indexes()]
    if INDEX_NAME not in existing:
        raise RuntimeError(
            f"Pinecone index '{INDEX_NAME}' not found. Run ingestion first"
        )
        
    return pc.Index(INDEX_NAME)

