# recommender/retriever.py

from transformers import pipeline, GenerationConfig
# from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import RetrievalQA,LLMChain
from langchain.prompts import PromptTemplate

from .utils import load_caregivers, build_vectorstore

# —————————————————————————————————————————————————————————
# 1. Load CSV & build FAISS retriever
docs = load_caregivers("caregivers.csv")
vectorstore = build_vectorstore(docs)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# —————————————————————————————————————————————————————————
# 2. Local HF pipeline→LLM wrapper
# hf_pipeline = pipeline(
#     "text-generation",
#     model="gpt2",
#     do_sample=False,
#     max_new_tokens=200,
# )

gen_config = GenerationConfig(
    do_sample=False,
    max_new_tokens=200,
     # you can set temperature here, e.g. temperature=0.7
 )
hf_pipeline = pipeline(
    "text-generation",
    model="gpt2",
    return_full_text=False,
)

hf_pipeline.model.generation_config = gen_config

llm = HuggingFacePipeline(pipeline=hf_pipeline)

# —————————————————————————————————————————————————————————
# 3. Build your custom prompt template
prompt = PromptTemplate(
    input_variables=["query", "context"],
    template="""
You are a professional, empathetic caregiver-matching assistant.
Given patient information and a list of caregiver profiles, recommend 2–3 suitable caregivers,
briefly explain why each was chosen, and never make jokes about age or health conditions.


**Output format (one per line, bullet):**  
- Name: <Caregiver Name>; Reason: <brief explanation>

Patient condition:
{query}

Caregiver profiles (for context):
{context}

""",
)

# —————————————————————————————————————————————————————————
# 4. Build your RetrievalQA chain using from_chain_type
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",
#     retriever=retriever,
#     return_source_documents=True,
#     chain_type_kwargs={"prompt": prompt},
#     input_key="query",
#     output_key="result",
# )
llm_chain = LLMChain(llm=llm, prompt=prompt)

# ——————————————————————————————
# (D) New helper to do RAG manually
def get_recommendations(query: str):
    # 1) retrieve top-3 caregiver docs (deprecated warning is OK for now)
    docs = retriever.get_relevant_documents(query)

    # 2) join their text for context
    context = "\n\n".join(d.page_content for d in docs)

    # 3) invoke the LLMChain with a single dict of inputs:
    output = llm_chain.invoke({
        "query": query,
        "context": context,
    })
    # the default output key for LLMChain is "text"
    answer = output["text"]

    return answer, docs
