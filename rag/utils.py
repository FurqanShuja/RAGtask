from rag.cache import ResponseCache
import hashlib

def generate_cache_key(query):
    """
    Generate a SHA-256 hash key for the given query.
    """
    return hashlib.sha256(query.encode('utf-8')).hexdigest()

def generate_prompt_with_exemplars(context, question, exemplars):
    """
    Generate a prompt string that includes exemplars for few-shot prompting.

    Args:
        context (str): The retrieved context from the document.
        question (str): The user's question.
        exemplars (list): List of exemplar dictionaries.

    Returns:
        str: The formatted prompt.
    """
    exemplar_text = ""
    for ex in exemplars:
        exemplar_text += f"Context: {ex['context']}\n"
        exemplar_text += f"Question: {ex['question']}\n"
        exemplar_text += f"Reasoning: {ex['reasoning']}\n"
        exemplar_text += f"Answer: {ex['answer']}\n\n"
    
    prompt = f"""
            Below are examples of how to answer questions with a chain of thought.

            {exemplar_text}

            Now, answer the following question with a detailed reasoning process.

            Context:
            {context}

            Question:
            {question}

            Reasoning:
            """
    return prompt
