from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.document_loaders import Docx2txtLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from paths import Paths
from langchain.llms import Ollama


def test_word():

    path = Paths().get_project_artifact("pdf", artifact="Татспиртпром.docx")
    loader = Docx2txtLoader(path)
    doc = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,  # Размер чанка
        chunk_overlap=500  # Перекрытие для контекста
    )
    chunks = text_splitter.split_documents(doc)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("faiss_index")

    llm = Ollama(model="qwen3:8b")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Просто вставляем чанки в промт
        retriever=db.as_retriever(search_kwargs={"k": 3})  # Берем 3 релевантных чанка
    )

    # Задаем вопрос
    question = "Процент размера аванса при превышении которого, размер обеспечения исполнения договора устанавливается в размере аванса"
    query_embedding = embeddings.embed_query(question)

    # Способ 1: через similarity_search
    print("Метод 1:")
    docs = db.similarity_search(question, k=2)
    for i, doc in enumerate(docs):
        print("=====")
        print(f"{i + 1}. {doc.page_content}")
