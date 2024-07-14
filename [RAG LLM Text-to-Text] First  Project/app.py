from flask import Flask, request, jsonify, render_template
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.requests import Requests as LangChainRequests

app = Flask(__name__)

def RAG_system():
    # load and process PDF
    loader = PyPDFLoader('Tulus_Setiawan_CV.pdf')
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # initialize GPT
    llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-0125')

    # create OpenAPI chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )

    return qa_chain

qa_chain = RAG_system()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = qa_chain({"question": user_input})
        return render_template('index.html', response=response['answer'])
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)