from utils import *
from langchain import document_loaders as dl
from langchain import text_splitter as ts
from langchain import embeddings
from langchain import vectorstores as vs
from langchain import retrievers
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from langchain import PromptTemplate



class TalkDocument():
    def __init__(self, data_source_path, OPENAI_KEY=None) -> None:
        self.data_source_path = data_source_path
        self.document = None
        self.document_splited = None
        self.embedding_model = None
        self.embedding_type = None
        self.OPENAI_KEY = OPENAI_KEY
        self.db = None
        self.llm = None
        self.chain = None
        self.repo_id = None

    

    def get_document(self, data_source_type="FILE"):
        data_source_type = data_source_type if data_source_type.upper() in DS_TYPE_LIST else DS_TYPE_LIST[0]

        if data_source_type == "FILE":
            loader = dl.TextLoader(self.data_source_path)
            self.document = loader.load()

        elif data_source_type == "PDF":
            loader = dl.PyPDFLoader(self.data_source_path)
            self.document = loader.load()

        elif data_source_type == "WEB":
            loader = dl.WebBaseLoader(self.data_source_path)
            self.document = loader.load()

        return self.document

    def get_split(self, split_type="character", chunk_size=1000, chunk_overlap=10):

        split_type = split_type.upper() if split_type.upper() in SPLIT_TYPE_LIST else SPLIT_TYPE_LIST[0]

        if self.document:

            if split_type == "CHARACTER":
                text_splitter = ts.RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            elif split_type == "TOKEN":
                text_splitter  = ts.TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            
            try:
                self.document_splited = text_splitter.split_documents(self.document)
            except Exception as error:
                print("An exception occurred:", error)

        return self.document_splited

    def get_embedding(self, embedding_type="HF", OPENAI_KEY=None):
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


        try:
            self.db = model_vectorstore.from_documents(self.document_splited, self.embedding_model)
        except Exception as error:
            print("An exception occurred:", error)

        return self.db
    
    def get_search(self, question, with_score=False):
        # TODO MultiQueryRetriever AND Max marginal relevance

        relevant_docs = None

        if self.db and "SVM" not in str(type(db)):

            if with_score:
                relevant_docs = self.db.similarity_search_with_relevance_scores(question)
            else:
                relevant_docs = self.db.similarity_search(question)
        elif self.db:
            relevant_docs = self.db.get_relevant_documents(question)
        
        return relevant_docs
    
    def get_response(self, question, repo_id="declare-lab/flan-alpaca-large", chain_type="stuff", relevant_docs=None, with_score=False, temperature=0, max_length=300):

        os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

        relevant_docs = self.get_search(question, with_score=with_score)

        self.repo_id = self.repo_id if self.repo_id is not None else repo_id
        chain_type = chain_type.lower() if chain_type.lower() in CHAIN_TYPE_LIST else CHAIN_TYPE_LIST[0]

        if (self.repo_id != repo_id ) or (self.llm is None):
             self.repo_id = repo_id 
             self.llm = HuggingFaceHub(repo_id=self.repo_id, model_kwargs=
                                                                        {"temperature":temperature,
                                                                        "max_length": max_length})
             
        prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Question: {question}
        Answer in Spanish:"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["question"]
        )


        self.chain = self.chain if self.chain is not None else load_qa_chain(self.llm, chain_type=chain_type, prompt_template=PROMPT)

        print(self.chain)

    
        response = self.chain({"input_documents": relevant_docs, "question": question})

        return response



         




        
        
        
    


    
import os 

# FILE
talkdocument_object = TalkDocument(data_source_path='./KS-all-info_rev1.txt')
talkdocument_object.get_document(data_source_type="FILE")
talkdocument_object.get_split(split_type="token", chunk_size=200)
embedding_model = talkdocument_object.get_embedding()
# print(embedding_model.embed_query("What is Hierarchy 4.0?"))
db = talkdocument_object.get_storage()
query = "What is the case study challenge"

# doct = talkdocument_object.get_search(query)

res = talkdocument_object.get_response(query)

print(res)

# print(db.similarity_search_by_vector(embedding_model.embed_query("What is Hierarchy 4.0?"))[0].page_content, "\n")

# print(db.similarity_search(query), "\n")
# print(db.get_relevant_documents(query), "\n")

# print(db.similarity_search_by_vector(query), "\n")
# print(db.similarity_search_with_relevance_scores(query), "\n")




# for doc in document:
#     print("%%%%", doc, "\n")
# PDF
# talkdocument_object = TalkDocument(data_source_path='./prueba.pdf', data_source_type="PDF")
# document = talkdocument_object.get_data()
# print(document)

#HTML
# urls = [
#     "https://python.langchain.com/docs/use_cases/question_answering/#step-1-load"
# ]
# talkdocument_object = TalkDocument(data_source_path=urls, data_source_type="WEB")
# document = talkdocument_object.get_data()
# print(document)




