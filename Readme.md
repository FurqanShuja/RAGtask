# Retrieval-Augmented Generation (RAG) Q&A System

A Q&A system using Retrieval-Augmented Generation (RAG) to answer questions based on the content of a provided document. The system combines document retrieval with a Large Language Model (LLM) to generate detailed responses.

---

## Project Structure

```
project/ <br/>
├── .env <br/>
├── requirements.txt <br/>
├── main.py <br/>
├── rag/ <br/>
│   ├── __init__.py <br/>
│   ├── retrieval.py <br/>
│   ├── generation.py <br/>
│   ├── cache.py <br/>
│   └── utils.py <br/>
├── exemplars/ <br/>
│   ├── __init__.py <br/>
│   └── exemplars.py <br/>
├── llm.py <br/>
└── doc.pdf <br/>
```

---

## How the Code Achieves the Tasks

### Base Tasks

#### Document Retrieval Setup
- **Files**: `rag/retrieval.py`
- **Description**:
  - **Loading Documents**: The `load_pdf_by_sections` function uses PyMuPDF to extract text from `doc.pdf`. It splits the document into sections based on the table of contents. If no table of contents is found, it treats the entire document as a single section.
  - **Text Splitting**: Utilizes `RecursiveCharacterTextSplitter` from LangChain to split the extracted text into manageable chunks, prioritizing splitting by paragraphs.
  - **Embedding and Indexing**: Uses `sentence-transformers` to generate embeddings for the text chunks. These embeddings are stored in a FAISS vector store for efficient retrieval.

#### LLM Integration
- **Files**: `llm.py`, `rag/generation.py`
- **Description**:
  - **Custom LLM Wrapper**: Defines a custom `GeminiLLM` class that wraps Google’s Gemini model to be compatible with LangChain.
  - **LLM Configuration**: Uses the `google-generativeai` package to configure and interact with the Gemini model.
  - **Response Generation**: The `ask_question` function in `rag/generation.py` uses the custom LLM to generate responses by passing both the user's query and the retrieved context.

#### Combining Retrieval and Generation (RAG)
- **Files**: `main.py`, `rag/generation.py`, `rag/retrieval.py`
- **Description**:
  - **User Interaction**: `main.py` handles user input and orchestrates the retrieval and generation process.
  - **Retrieval**: Retrieves the most relevant passages using the FAISS retriever based on semantic similarity.
  - **Generation**: Combines the retrieved context with the user's question and feeds it into the LLM to generate a detailed and accurate response.

---

### Additional Tasks (Bonus Points)

#### Advanced Retrieval
- **Description**: Implements semantic search using vector embeddings from `sentence-transformers` and FAISS. This allows the retriever to find documents based on semantic similarity rather than keyword matching.

#### Clarification Mechanism
- **Files**: `rag/generation.py`
- **Description**: If the retrieval confidence is below a predefined threshold, the system informs the user that it couldn't find relevant information. It then prompts the user for clarification, improving the chances of retrieving relevant information in the next attempt.

#### Chain of Thought
- **Files**: `exemplars/exemplars.py`, `rag/utils.py`, `rag/generation.py`
- **Description**: Provides exemplars that demonstrate how to answer questions with a detailed reasoning process. The `generate_prompt_with_exemplars` function constructs a prompt that includes these exemplars, encouraging the LLM to produce step-by-step reasoning in its answers.

#### Response Caching
- **Files**: `rag/cache.py`, `rag/generation.py`, `rag/utils.py`
- **Description**: Implements a simple caching mechanism using a hash of the user’s query as the key. Stores responses for frequently asked questions to optimize retrieval and reduce redundant computation.

---

## How to Run the Code

### 1. Clone the Repository
```bash
git clone <repository-url>
cd project/ 
```

### 2. Install Dependencies
Ensure you have Python 3.7+ installed.

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root directory.

Add your Gemini API key to the `.env` file:

```makefile
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Add the Document
Place `doc.pdf` (the document you want to use for retrieval) in the project root directory.

Ensure that the file path in `main.py` is correct:

```python
file_path = "doc.pdf"
```

### 5. Run the Application
To start the application, run:

```bash
python main.py
```

## Example Usage

When you run `main.py`, the system welcomes you to the Q&A interface, explaining how to interact with it. After entering a question (e.g., "Can you explain blockchain?"), the system performs a retrieval and generation step, displaying information from the document as well as an AI-generated answer.

```plaintext
Welcome to the RAG (Retrieval-Augmented Generation) Q&A System!
You can ask any question based on the provided document.
Type 'exit' or 'quit' to terminate the program.

--------------------------------------------------

Please enter your question (or type 'exit' to quit): what are smart contracts

--- Retrieval Step ---
Retrieved from 'Document':
"healthcare, and digital identity management, among others. Smart contracts, which are
self-executing contracts with the terms of the agreement directly written into code, are one
of the most exciting developments in the blockchain space, enabling automated and
trustless transactions."


--- Answer Generation ---
Reasoning:
Meaning: Smart contracts are self-executing agreements written in code that automate and secure transactions on a blockchain.
Categories/Types: They can be categorized into different types based on their functionality, such as simple contracts for basic transactions or more complex contracts involving multiple parties and conditions.
Applications: Smart contracts have numerous applications including automated payments, supply chain management, and decentralized finance (DeFi).

Answer:
Smart contracts are self-executing agreements written in code that automate and secure transactions on a blockchain. They can be categorized into different types based on their functionality, such as simple contracts for basic transactions or more complex contracts involving multiple parties and conditions. Smart contracts have numerous applications including automated payments, supply chain management, and decentralized finance (DeFi).

--------------------------------------------------

Please enter your question (or type 'exit' to quit): where can i find butterflies?
I'm sorry, I couldn't find any relevant information to answer your question.
Could you please provide more details or clarify your question?

Please clarify your question: exit
Exiting the program. Goodbye!
```

--------------------------------------------------