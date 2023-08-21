from langchain import document_loaders as dl
from langchain import text_splitter as ts
from langchain import embeddings
from langchain import vectorstores as vs
from langchain import retrievers
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from langchain import PromptTemplate

# Some constant
DS_TYPE_LIST = ["WEB", "PDF", "TXT"]
SPLIT_TYPE_LIST = ["CHARACTER", "TOKEN"]
EMBEDDING_TYPE_LIST = ["HF", "OPENAI"]
VECTORSTORE_TYPE_LIST = ["FAISS", "CHROMA", "SVM"]
REPO_ID_DEFAULT = "declare-lab/flan-alpaca-large"
CHAIN_TYPE_LIST = ["stuff", "map_reduce", "map_rerank", "refine"]


class TalkDocument(object):
    """
    TalkDocument is a class for processing and interacting with documents, embeddings, and question-answering chains.

    Attributes:
        data_source_path (str): Path to the data source (TXT, PDF, or web URL).
        HF_API_TOKEN (str): Hugging Face API token.
        OPENAI_KEY (str): OpenAI API key.
        document (str): Loaded document content.
        document_splited (list): List of document chunks after splitting.
        embedding_model (EmbeddingsBase): Embedded model instance.
        embedding_type (str): Type of embedding model used (HF or OPENAI).
        db (VectorStoreBase): Vector storage instance.
        llm (HuggingFaceHub): Hugging Face Hub instance.
        chain (QuestionAnsweringChain): Question answering chain instance.
        repo_id (str): Repository ID for Hugging Face models.

    Methods:
        get_document(data_source_type="TXT"): Load the document content based on the data source type.
        get_split(split_type="character", chunk_size=1000, chunk_overlap=10): Split the document content into chunks.
        get_embedding(embedding_type="HF", OPENAI_KEY=None): Get the embedding model based on the type.
        get_storage(vectorstore_type="FAISS", embedding_type="HF", OPENAI_KEY=None): Create vector storage using embeddings.
        get_search(question, with_score=False): Perform a similarity search for relevant documents.
        do_question(question, repo_id="declare-lab/flan-alpaca-large", chain_type="stuff", relevant_docs=None, with_score=False, temperature=0, max_length=300, language="Spanish"): Answer a question using relevant documents and a question-answering chain.
        create_db_document(data_source_type="TXT", split_type="token", chunk_size=200, embedding_type="HF", chunk_overlap=10, OPENAI_KEY=None, vectorstore_type="FAISS"): Create and return a vector storage instance with document content.
    """
    def __init__(self, HF_API_TOKEN, data_source_path=None, data_text=None, OPENAI_KEY=None) -> None:
        """
        Initialize the TalkDocument instance.

        :param data_source_path: Path to the data source (TXT, PDF, or web URL).
        :type data_source_path: str
        :param HF_API_TOKEN: Hugging Face API token.
        :type HF_API_TOKEN: str
        :param OPENAI_KEY: OpenAI API key.
        :type OPENAI_KEY: str, optional
        """
        self.data_source_path = data_source_path
        self.data_text = data_text
        self.document = None
        self.document_splited = None
        self.embedding_model = None
        self.embedding_type = None
        self.OPENAI_KEY = OPENAI_KEY
        self.HF_API_TOKEN = HF_API_TOKEN
        self.db = None
        self.llm = None
        self.chain = None
        self.repo_id = None

        if not self.data_source_path and not self.data_text:
            #TODO ADD LOGS
            print("YOU MUST INTRODUCE ONE OF THEM")

    

    def get_document(self, data_source_type="TXT"):
        """
        Load the document content based on the data source type.

        :param data_source_type: Type of data source (TXT, PDF, WEB).
        :type data_source_type: str, optional
        :return: Loaded document content.
        :rtype: str
        """
        data_source_type = data_source_type if data_source_type.upper() in DS_TYPE_LIST else DS_TYPE_LIST[0]
        if data_source_type == "TXT":
            if self.data_text:
                self.document = self.data_text
            elif self.data_source_path:
                loader = dl.TextLoader(self.data_source_path)
                self.document = loader.load()

        elif data_source_type == "PDF":
            if self.data_text:
                self.document = self.data_text
            elif self.data_source_path:
                loader = dl.PyPDFLoader(self.data_source_path)
                self.document = loader.load()

        elif data_source_type == "WEB":
            loader = dl.WebBaseLoader(self.data_source_path)
            self.document = loader.load()

        return self.document

    def get_split(self, split_type="character", chunk_size=200, chunk_overlap=10):
        """
        Split the document content into chunks.

        :param split_type: Type of splitting (character, token).
        :type split_type: str, optional
        :param chunk_size: Size of each chunk.
        :type chunk_size: int, optional
        :param chunk_overlap: Overlap size between chunks.
        :type chunk_overlap: int, optional
        :return: List of document chunks after splitting.
        :rtype: list
        """

        split_type = split_type.upper() if split_type.upper() in SPLIT_TYPE_LIST else SPLIT_TYPE_LIST[0]

        if self.document:

            if split_type == "CHARACTER":
                text_splitter = ts.RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            elif split_type == "TOKEN":
                text_splitter  = ts.TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
 
            if self.data_text:
                try:
                    self.document_splited = text_splitter.split_text(text=self.document)
                except Exception as error:
                    print(f"Error in split data text step: {error}")

            elif self.data_source_path:
                try:
                    self.document_splited = text_splitter.split_documents(documents=self.document)
                except Exception as error:
                     print(f"Error in split data source step: {error}")
        
        return self.document_splited

    def get_embedding(self, embedding_type="HF", OPENAI_KEY=None):
        """
        Get the embedding model based on the type.

        :param embedding_type: Type of embedding model (HF, OPENAI).
        :type embedding_type: str, optional
        :param OPENAI_KEY: OpenAI API key.
        :type OPENAI_KEY: str, optional
        :return: Embedded model instance.
        :rtype: EmbeddingsBase
        """
        if not self.embedding_model:

            embedding_type = embedding_type.upper() if embedding_type.upper() in EMBEDDING_TYPE_LIST else EMBEDDING_TYPE_LIST[0]

            if embedding_type == "HF":
                self.embedding_model = embeddings.HuggingFaceEmbeddings()

            elif embedding_type == "OPENAI":
                self.OPENAI_KEY = self.OPENAI_KEY if self.OPENAI_KEY else OPENAI_KEY
                if self.OPENAI_KEY:
                    self.embedding_model = embeddings.OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
                else:
                    print("You need to introduce a OPENAI API KEY")

            self.embedding_type = embedding_type

            return self.embedding_model
    
    def get_storage(self, vectorstore_type = "FAISS", embedding_type="HF", OPENAI_KEY=None):
        """
        Create vector storage using embeddings.

        :param vectorstore_type: Type of vector storage (FAISS, CHROMA, SVM).
        :type vectorstore_type: str, optional
        :param embedding_type: Type of embedding model (HF, OPENAI).
        :type embedding_type: str, optional
        :param OPENAI_KEY: OpenAI API key.
        :type OPENAI_KEY: str, optional
        :return: Vector storage instance.
        :rtype: VectorStoreBase
        """

        self.embedding_type = self.embedding_type if self.embedding_type else embedding_type
        vectorstore_type = vectorstore_type.upper() if vectorstore_type.upper() in VECTORSTORE_TYPE_LIST else VECTORSTORE_TYPE_LIST[0]

        self.get_embedding(embedding_type=self.embedding_type, OPENAI_KEY=OPENAI_KEY)

        if vectorstore_type == "FAISS":
            model_vectorstore = vs.FAISS

        elif vectorstore_type == "CHROMA":
            model_vectorstore = vs.Chroma

        elif vectorstore_type == "SVM":
            model_vectorstore = retrievers.SVMRetriever

        # TODO
        # elif vectorstore_type == "LANCE":
        #     model_vectorstore = vs.LanceDB

        if self.data_text:
            try:
                self.db = model_vectorstore.from_texts(self.document_splited, self.embedding_model)
            except Exception as error:
                print(f"Error in storage data text step: {error}")
                self.db = None

        elif self.data_source_path:
            try:
                self.db = model_vectorstore.from_documents(self.document_splited, self.embedding_model)
            except Exception as error:
                print(f"Error in storage data source step: {error}")
                self.db = None

        return self.db
    
    def get_search(self, question, with_score=False):
        """
        Perform a similarity search for relevant documents.

        :param question: Question text.
        :type question: str
        :param with_score: Flag indicating whether to include relevance scores.
        :type with_score: bool, optional
        :return: Relevant documents or document indices.
        :rtype: list or ndarray
        """

        # TODO MultiQueryRetriever AND Max marginal relevance

        relevant_docs = None

        if self.db and "SVM" not in str(type(self.db)):

            if with_score:
                relevant_docs = self.db.similarity_search_with_relevance_scores(question)
            else:
                relevant_docs = self.db.similarity_search(question)
        elif self.db:
            relevant_docs = self.db.get_relevant_documents(question)
        
        return relevant_docs
    
    def do_question(self, 
                     question,
                     repo_id="declare-lab/flan-alpaca-large", 
                     chain_type="stuff", 
                     relevant_docs=None, 
                     with_score=False, 
                     temperature=0, 
                     max_length=300, 
                     language="Spanish"):
        """
        Answer a question using relevant documents and a question-answering chain.

        :param question: Question text.
        :type question: str
        :param repo_id: Repository ID for Hugging Face models.
        :type repo_id: str, optional
        :param chain_type: Type of question-answering chain (stuff, ...).
        :type chain_type: str, optional
        :param relevant_docs: Relevant documents or document indices.
        :type relevant_docs: list or ndarray, optional
        :param with_score: Flag indicating whether to include relevance scores.
        :type with_score: bool, optional
        :param temperature: Sampling temperature for generating answers.
        :type temperature: float, optional
        :param max_length: Maximum length of generated answers.
        :type max_length: int, optional
        :param language: Language of the answer.
        :type language: str, optional
        :return: Answer to the question.
        :rtype: str
        """

        relevant_docs = self.get_search(question, with_score=with_score)
        if relevant_docs:

            self.repo_id = self.repo_id if self.repo_id is not None else repo_id
            chain_type = chain_type.lower() if chain_type.lower() in CHAIN_TYPE_LIST else CHAIN_TYPE_LIST[0]


            if (self.repo_id != repo_id ) or (self.llm is None):
                self.repo_id = repo_id 
                self.llm = HuggingFaceHub(repo_id=self.repo_id,huggingfacehub_api_token=self.HF_API_TOKEN,
                                            model_kwargs=
                                            {"temperature":temperature,
                                            "max_length": max_length})
                
            prompt_template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            If the question is similar to [Talk me about the document], 
            the response should be a summary commenting on the most important points about the document


            {context}
            Question: {question}
            """
            PROMPT = PromptTemplate(
                template=prompt_template, input_variables=["context", "question"]
            )
            PROMPT = PROMPT  + f" The Answer have to be in  {language} language:"


            self.chain = self.chain if self.chain is not None else load_qa_chain(self.llm, chain_type=chain_type, prompt = PROMPT)

            response = self.chain({"input_documents": relevant_docs, "question": question}, return_only_outputs=True)

            return response
        
        else:
            return {"output_text": "ERROR: Something went wrong and the query could not be performed. Check the data source and its access"}
    
    

    def create_db_document(self, 
                           data_source_type="TXT",
                           split_type="token",
                           chunk_size=200,
                           embedding_type="HF",
                           chunk_overlap=10,
                           OPENAI_KEY=None,
                           vectorstore_type = "FAISS"):
        """
        Create and return a vector storage instance with document content.

        :param data_source_type: Type of data source (TXT, PDF, WEB).
        :type data_source_type: str, optional
        :param split_type: Type of splitting (token, character).
        :type split_type: str, optional
        :param chunk_size: Size of each chunk.
        :type chunk_size: int, optional
        :param embedding_type: Type of embedding model (HF, OPENAI).
        :type embedding_type: str, optional
        :param chunk_overlap: Overlap size between chunks.
        :type chunk_overlap: int, optional
        :param OPENAI_KEY: OpenAI API key.
        :type OPENAI_KEY: str, optional
        :param vectorstore_type: Type of vector storage (FAISS, CHROMA, SVM).
        :type vectorstore_type: str, optional
        :return: Vector storage instance.
        :rtype: VectorStoreBase
        """
        
        self.get_document(data_source_type=data_source_type)
        self.get_split(split_type=split_type, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        db = self.get_storage(vectorstore_type=vectorstore_type, embedding_type=embedding_type, OPENAI_KEY=OPENAI_KEY)
    
        return db
    

# ********************************** EXAMPLE **********************************
# obj = TalkDocument(HF_API_TOKEN = "YOURKEY",data_source_path="data/test.txt")
# obj.create_db_document()

# question = "What is Hierarchy 4.0?"
# res  = obj.do_question(question=question, language="ENGLISH")
# print(res)

"""
RESPONSE: 

{'output_text': "Hierarchy 4.0 is an innovative software solution for control Safety Systems. It provides an interactive diagram of the entire plant revealing cause and effect Behavior with readings provided in a hierarchical view allowing for a deep understanding of the system's strategy. All data is collected from multiple sources visualized as a diagram and optimized through a customized dashboard allowing users to run a logic simulation from live data or pick a moment from their history. Your simulation is based on actual safety Logics not just on a math model."}

"""


      
