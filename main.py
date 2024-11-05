import os
from dotenv import load_dotenv
from rag.retrieval import (
    load_pdf_by_sections,
    setup_retriever
)
from rag.generation import ask_question
from exemplars.exemplars import EXEMPLARS

def main():
    # Load environment variables
    load_dotenv()
    
    # Load the document using PyMuPDF
    file_path = "doc.pdf"  # Ensure this path is correct
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    documents = load_pdf_by_sections(file_path)
    
    # Setup the retriever with the documents and exemplars
    retriever, knowledge_base = setup_retriever(documents)
    
    # Introduction and Instructions
    print("Welcome to the RAG (Retrieval-Augmented Generation) Q&A System!")
    print("You can ask any question based on the provided document.")
    print("Type 'exit' or 'quit' to terminate the program.\n")
    
    while True:
        # Prompt the user for a question
        question = input("Please enter your question (or type 'exit' to quit): ").strip()
        
        # Check if the user wants to exit
        if question.lower() in ['exit', 'quit']:
            print("Exiting the program. Goodbye!")
            break
        
        # Ensure the user entered a non-empty question
        if not question:
            print("You entered an empty question. Please try again.\n")
            continue
        
        # Use the ask_question function
        answer = ask_question(question, retriever, knowledge_base, EXEMPLARS)
        
        # Display the Answer Generation Step
        print("\n--- Answer Generation ---")
        print(answer)
        print("\n" + "-"*50 + "\n")  # Separator for readability

if __name__ == "__main__":
    main()
