from flask import Flask, request, jsonify

from langchain.prompts.prompt import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import re


app = Flask(__name__)


model_name = "llama3.1"  # Adjust to the actual model you are using

@app.route('/calculateToken', methods=['POST'])
def calculate_token():
   
    data = request.get_json()
    
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    print(prompt)
    
    token_count = loopkup(prompt)
    
    return jsonify({"token_count": token_count})


def loopkup(name:str)-> str:
    print("Starting Ollama")

    summary_template = "Count the total number of tokens in {format_instructions}. Return only integer total count. Just give total count only "

    format_instructions  = name
    
    summary_prompt_template = PromptTemplate(
        input_variables=["format_instructions"], template=summary_template
    )

    print(summary_template)

    llm = ChatOllama(model="llama3.1")
    chain = summary_prompt_template | llm | StrOutputParser()
    
    res = chain.invoke(input={"format_instructions": format_instructions})
    print(res)
    return res



if __name__ == '__main__':
    app.run(debug=True, port=8081)
