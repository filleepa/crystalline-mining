from pymilvus import MilvusClient, DataType

client = MilvusClient(uri="http://localhost:19530/")

# create schema
schema = MilvusClient.create_schema()

schema.add_field(
    field_name="id",
    datatype=DataType.INT64,
    is_primary=True,
    auto_id=True
)

schema.add_field(
    field_name="embeddings",
    datatype=DataType.FLOAT_VECTOR,
    dim=384
)

schema.add_field(
    field_name="text",
    datatype=DataType.VARCHAR,
    max_length=65535
)

# set index parameters
index_params = client.prepare_index_params()

index_params.add_index(
    field_name="id",
    index_type="AUTOINDEX"
)

index_params.add_index(
    field_name="embeddings",
    index_type="AUTOINDEX",
    metric_type="COSINE"
)


# create collection
client.create_collection(
    collection_name="crystalline_papers",
    schema=schema,
    index_params=index_params,
    enable_dynamic_field=True
)

res = client.get_load_state(
    collection_name="crystalline_papers"
)

print(res)