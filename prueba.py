from utils import *
from langchain import document_loaders as dl
from langchain import text_splitter as ts



class TalkDocument():
    def __init__(self, data_source_path) -> None:
        self.data_source_path = data_source_path
        self.document = ""

    

    def get_data(self, data_source_type="FILE"):
        data_source_type = data_source_type if data_source_type.upper() in DS_TYPE_LIST else DS_TYPE_LIST[0]

        document = ""

        if data_source_type == "FILE":
            loader = dl.TextLoader(self.data_source_path)
            document = loader.load()

        elif data_source_type == "PDF":
            loader = dl.PyPDFLoader(self.data_source_path)
            document = loader.load()

        elif data_source_type == "WEB":
            loader = dl.WebBaseLoader(self.data_source_path)
            document = loader.load()
        
        self.document = document

    def get_split(self, split_type="character", chunk_size=1000, chunk_overlap=10):

        document_splited = ""
        split_type = split_type.upper() if split_type.upper() in SPLIT_TYPE_LIST else SPLIT_TYPE_LIST[0]

        
        if self.document:

            if split_type == "CHARACTER":
                text_splitter = ts.RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                document_splited = text_splitter.split_documents(self.document)
            elif split_type == "TOKEN":
                text_splitter  = ts.TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                document_splited = text_splitter.split_documents(self.document)
    

        return document_splited







    


# FILE
# talkdocument_object = TalkDocument(data_source_path='./KS-all-info_rev1.txt')
# talkdocument_object.get_data(data_source_type="FILE")
# document = talkdocument_object.get_split(split_type="token", chunk_size=200)

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




