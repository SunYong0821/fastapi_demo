from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.vllm import VLLMEmbedder
from agno.vectordb.pgvector import PgVector, SearchType

db_url = "postgresql+psycopg://ai:ai@localhost:5432/ai"
db = PostgresDb(db_url=db_url)

whu_c_db = PostgresDb(db_url=db_url, knowledge_table="whu_medimmune_c")
whu_v_db = PgVector(
    db_url=db_url,
    table_name='whu_medimmune_v',
    search_type=SearchType.hybrid,
    vector_score_weight=0.9,
    embedder=VLLMEmbedder(
        id='qw3embed',
        base_url='http://localhost:10000/v1',
        api_key='EMPTY',
        dimensions=2560
    )
)
whu_db = Knowledge(vector_db=whu_v_db, contents_db=whu_c_db, max_results=5)

ksd_project_c_db = PostgresDb(db_url=db_url, knowledge_table="project_info_c")
ksd_project_v_db = PgVector(
    db_url=db_url,
    table_name='project_info_v',
    search_type=SearchType.hybrid,
    vector_score_weight=0.9,
    embedder=VLLMEmbedder(
        id='qw3embed',
        base_url='http://localhost:10000/v1',
        api_key='EMPTY',
        dimensions=2560
    )
)
ksd_project_db = Knowledge(vector_db=ksd_project_v_db, contents_db=ksd_project_c_db, max_results=5)

ksd_sample_c_db = PostgresDb(db_url=db_url, knowledge_table="recommend_sample_c")
ksd_sample_v_db = PgVector(
    db_url=db_url,
    table_name='recommend_sample_v',
    search_type=SearchType.hybrid,
    vector_score_weight=0.9,
    embedder=VLLMEmbedder(
        id='qw3embed',
        base_url='http://localhost:10000/v1',
        api_key='EMPTY',
        dimensions=2560
    )
)
ksd_sample_db = Knowledge(vector_db=ksd_sample_v_db, contents_db=ksd_sample_c_db, max_results=5)
