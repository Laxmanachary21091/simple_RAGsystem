# 1. DOCUMENT STORE - Simple corpus
corpus = [
    "Python is a programming language",
    "JavaScript is used for web development",
    "Machine Learning uses AI algorithms"
]

# 2. RETRIEVER - Embedding-based retrieval
from sentence_transformers import SentenceTransformer
retriever_model = SentenceTransformer('all-MiniLM-L6-v2')
corpus_embeddings = retriever_model.encode(corpus)

# 3. ORCHESTRATION - Query processing
def rag_pipeline(user_query):
    # Retrieve
    query_embedding = retriever_model.encode(user_query)
    scores = corpus_embeddings @ query_embedding
    top_k_indices = scores.argsort()[-3:][::-1]
    retrieved_docs = [corpus[i] for i in top_k_indices]
    
    # Rerank (optional - here we just use top results)
    reranked_docs = retrieved_docs[:2]
    
    # Generate context
    context = "\n".join(reranked_docs)
    
    return context, reranked_docs

# 4. GENERATOR - Answer generation
from transformers import pipeline
generator = pipeline("text-generation", model="gpt2")

query = "What is Python?"
context, docs = rag_pipeline(query)

prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
answer = generator(prompt, max_length=50)

print(f"Retrieved Docs: {docs}")
print(f"Generated Answer: {answer[0]['generated_text']}")
