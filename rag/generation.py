from langchain.chains import RetrievalQA
from llm import custom_gemini_llm  # Use the custom Gemini LLM
from rag.utils import generate_prompt_with_exemplars
from rag.cache import ResponseCache
from rag.utils import generate_cache_key
import hashlib

def ask_question(query, retriever, knowledge_base, exemplars):
    """
    Ask a question using the RetrievalQA chain with Few-Shot Chain of Thought.

    """
    # Initialize the response cache
    response_cache = ResponseCache()
    
    # Check if the response is in the cache
    cache_key = generate_cache_key(query)
    cached_answer = response_cache.get(cache_key)
    if cached_answer:
        print("Retrieving answer from cache.")
        return cached_answer
    
    # Retrieve relevant documents with scores
    docs_and_scores = knowledge_base.similarity_search_with_score(query, k=1)
    
    if docs_and_scores:
        top_doc, top_score = docs_and_scores[0]

        # Adjust the confidence threshold as needed
        confidence_threshold = 0.7  
        
        if top_score <= confidence_threshold:

            # Proceed if the retrieval confidence is high enough
            relevant_passage = top_doc.page_content.strip()
            source = top_doc.metadata.get("source", "Unknown Source")
            
            # Display the Retrieval Step
            print("\n--- Retrieval Step ---")
            print(f"Retrieved from '{source}':")
            print(f"\"{relevant_passage}\"\n")
            
            # Generate the prompt with exemplars
            prompt = generate_prompt_with_exemplars(relevant_passage, query, exemplars)
            
            # Initialize the RetrievalQA chain with the custom Gemini LLM and the retriever
            qa_chain = RetrievalQA.from_chain_type(
                llm=custom_gemini_llm,  
                chain_type="stuff",  
                retriever=retriever, 
                return_source_documents=True  
            )
            
            # Generate the answer using the RetrievalQA chain
            result = qa_chain.invoke({"query": prompt})
            
            # Extract the answer
            answer = result['result']
            
            # Cache the response
            response_cache.set(cache_key, answer)
            
            return answer
        else:
            # If retrieval confidence is low, initiate the clarification mechanism
            print("I'm sorry, I couldn't find any relevant information to answer your question.")
            print("Could you please provide more details or clarify your question?\n")
            
            # Prompt the user for clarification
            clarification = input("Please clarify your question: ").strip()
            
            if clarification.lower() in ['exit', 'quit']:
                print("Exiting the program. Goodbye!")
                exit()
            
            if not clarification:
                print("You entered an empty clarification. Please try again.\n")
                return "I'm sorry, I couldn't find any relevant information to answer your question."
            
            # Recursive call with the clarified query
            return ask_question(clarification, retriever, knowledge_base, exemplars)
    else:
        print("\nNo relevant passages found.")
        return "I'm sorry, I couldn't find any information related to your question."
