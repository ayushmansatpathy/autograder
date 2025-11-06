from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from os import getenv
from time import sleep

class PineconeClient:
    """
    This class initializs a Pinecone client connection to interact with the Pinecone
    rubric embeddings index. Supports CRUD operations.
    """

    def __init__(self):
        """
        Initializes a Pinecone connection and creates the rubric embeddings index if it does not exist.
        """
        load_dotenv("../../.env")
        API_KEY = getenv("PINECONE_API_KEY")
        INDEX_NAME = "rubric-embeddings"
        self._pc = Pinecone(api_key=API_KEY)

        if INDEX_NAME not in self._pc.list_indexes().names():
            self._pc.create_index(
                name=INDEX_NAME,
                dimension=384,  # Dimension of all-MiniLM-L6-v2 SentenceTransformer model vector embeddings
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            # Wait for index to be ready
            while not self._pc.describe_index(INDEX_NAME).status["ready"]:
                sleep(1)

        self._index = self._pc.Index(INDEX_NAME)

    def upsert_vectors(self, vectors, user_id):
        """
        Upserts (Update and Insert) vectors into the specified user namespace of
        the rubric embeddings index. Creates a namespace for a user if it does not exist.

        Args:
            vectors (list): List of tuples (id: str, embedding: List[float], metadata: Dict[Any : Any]) to upsert.
            user_id (str): The UUID of the user whose vectors are associated with.
        """
        self._index.upsert(vectors, user_id)

    def query_data(self, user_id, query_vector):
        """
        Queries the index for the top 5 most similar vectors to `query_vector` and returns their associated
        data. Only looks at the namespace of the specified user.

        Args:
            user_id (str): The UUID of the user whose namespace to look at.
            query_vector (tuple): The vector of form (id: str, embedding: List[float], metadata: Dict[Any : Any])
            to match with.

        Returns:
            QueryResponse object which contains the list of the top 5 closest vectors as ScoredVector objects,
            and namespace name.
        """
        return self._index.query(
            namespace=user_id,
            vector=query_vector,
            top_k=5,
            include_metadata=True,
            include_values=True,
        )

    def delete_namespace(self, user_id):
        """
        Delets the entire namepsace associated with the `user_id`. All data associated with the `user_id`
        namepsace is removed.

        Args:
            user_id (str): The UUID of the user whose namepsace to delete.
        """
        self._index.delete(delete_all=True, namespace=user_id)

    def delete_vectors(self, user_id, vector_ids):
        """
        Deletes specific vectors associated with the `user_id` in the namespace.
        Only the vectors with the provided IDs are removed, not the entire namespace.

        Args:
            user_id (str): The user ID associated with the namespace.
            vector_ids (list): A list of vector IDs to be deleted from the namespace.
        """
        self._index.delete(ids=vector_ids, namespace=user_id)
