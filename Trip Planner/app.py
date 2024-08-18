from flask import Flask, request, render_template
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from markdown import markdown
import re


app = Flask(__name__)

def agents_system():
    llm = ChatOpenAI(temperature=0.2, model="gpt-4o-mini")
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create messages for the language model
    system_message = """
    You are an AI vacation planner assistant. Your task is to recommend vacation plans based on the user's input. 
    Use the provided search results from traveloka.com as a reference for your recommendations. 
    
    Provide your recommendations in the following format:
    1. Hotel recommendation
    2. Flight recommendation (if applicable)
    3. Activities or places to visit
    4. Brief description of the destination
    5. Estimated budget that needs to be prepared

    Remember to be specific and provide actual names of hotels, flights, and activities when possible.
    Make sure that the text bold level for the section title and the body or list is different. Each list should be written on a new line!
    """
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('human', '{input}')
    ])
        
    chain = LLMChain(
        llm=llm,
        memory=memory,
        prompt=chat_prompt,
        verbose=True
    )
        
    return chain

def truncate_prompt(prompt, max_length=1000):
    if len(prompt) <= max_length:
        return prompt
    return prompt[:max_length-3] + "..."

def image_generator_system():
    llm = OpenAI(temperature=0.2)
    prompt = PromptTemplate(
        input_variables=['image_desc'],
        template='Generate a detailed prompt (maximum 500 characters) to generate an image with highest quality, no noise, no watermarks, and clear based on the following description: {image_desc}'
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    
    def generate_image(image_desc):
        generated_prompt = chain.invoke(image_desc)
        truncated_prompt = truncate_prompt(generated_prompt['text'], 1000)
        image_url = DallEAPIWrapper(quality='hd').run(truncated_prompt)
        return image_url

    return generate_image

def parse_places_to_visit(ai_response):
    # Find the places to visit section
    places_section = re.search(r'(?s)3\. Activities or Places to Visit.*?(?=\d\.|\Z)', ai_response)
    
    if not places_section:
        return "Activities or Places to Visit not found in the response."
    
    places_info = places_section.group(0)
    
    # Extract activities or places
    activities = re.findall(r'- \*\*(.*?)\*\*\s+(.*?)(?=- \*\*|\Z)', places_info, re.DOTALL)
    
    if not activities:
        return "No activities or places found in the section."
    
    # Format the extracted information
    parsed_info = "Activities or Places to Visit:\n"
    for place, description in activities:
        parsed_info += f"- {place.strip()}\n"
        parsed_info += f"  {description.strip()}\n"
    
    return parsed_info.strip()

def parse_hotel_recommendations(ai_response):
    # Find the hotel recommendations section
    hotel_section = re.search(r'(?s)1\. Hotel Recommendation.*?(?=\d\.|\Z)', ai_response)
    
    if not hotel_section:
        return "Hotel Recommendation not found in the response."
    
    hotel_info = hotel_section.group(0)
    
    # Extract hotel name and description
    hotel_match = re.search(r'- \*\*(.*?)\*\*\s+(.*?)(?=\n\n|\Z)', hotel_info, re.DOTALL)
    
    if not hotel_match:
        return "No hotel information found in the section."
    
    hotel_name, hotel_description = hotel_match.groups()
    
    # Format the extracted information
    parsed_info = "Hotel Recommendation:\n"
    parsed_info += f"- {hotel_name.strip()}\n"
    parsed_info += f"  {hotel_description.strip()}"
    
    return parsed_info.strip()

chain = agents_system()
dalle_system = image_generator_system()
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global chat_history
    if request.method == 'POST':
        user_input = request.form['user_input']
        chat_history.append({"type": "user", "content": user_input})

        # process the query
        response = chain.invoke({'input':user_input})
        ai_response = response['text']
        html = markdown(ai_response)

        # Get image URL
        parsed_hotel_info = parse_hotel_recommendations(ai_response)
        image_url1 = dalle_system(parsed_hotel_info)
        parsed_places_info = parse_places_to_visit(ai_response)
        image_url2 = dalle_system(parsed_places_info)

        chat_history.append({"type": "system", "content": html, "image_url1": image_url1, "image_url2": image_url2})
        
        return render_template('user_interface.html', chat_history=chat_history)
    
    return render_template('user_interface.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)