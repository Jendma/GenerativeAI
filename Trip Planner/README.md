# Proof of Concept: AI-Powered Vacation Planner Assistant

## 1. Project Overview

The AI-Powered Vacation Planner Assistant is an innovative solution designed to autonomously plan vacations for users based on their input prompts. This system leverages advanced AI technologies to provide personalized vacation recommendations, including accommodations, activities, and visual representations of suggested destinations.

## 2. Objectives

- Create an AI-driven system capable of generating comprehensive vacation plans
- Provide users with tailored recommendations for hotels, flights, activities, and destinations
- Integrate image generation to visually represent recommended locations
- Develop a user-friendly interface for interaction with the AI assistant
- Implement a connection to travel booking platforms for seamless reservation processes

## 3. Technology Stack

### 3.1 AI and Machine Learning
- **Language Model**: OpenAI API (GPT-4o-mini)
- **Image Generation**: OpenAI API (DALL-E)
- **Framework**: LangChain

### 3.2 Backend
- **Programming Language**: Python
- **Web Framework**: Flask

### 3.3 Frontend
- **Markup**: HTML
- **Styling**: CSS (assumed, based on class names in HTML)

### 3.4 Deployment
- **Containerization**: Docker
- **Orchestration**: Docker Compose

## 4. Key Features

### 4.1 Implemented Features
1. **AI-Powered Recommendations**
   - Utilizes GPT-4o-mini to process user inputs and generate vacation plans
   - Implements system prompts to structure AI responses

2. **Image Generation**
   - Uses DALL-E to create visual representations of recommended hotels and destinations

3. **User Interface**
   - Displays AI-generated recommendations with both text and images
   - Provides a button linking to Traveloka for booking actions

4. **Conversation Memory**
   - Maintains context throughout the user interaction using ConversationBufferMemory

5. **Response Parsing**
   - Extracts specific information about hotel recommendations and places to visit

### 4.2 Planned Features (Not Yet Implemented)
1. Integration with personal accounts (e.g., Google account)
2. Payment gateway for direct bookings
3. Connection to personal calendars (e.g., Google Calendar) for automated schedule syncing

## 5. System Architecture

```
[User] <-> [Flask Web App] <-> [LangChain Framework]
                                      |
                                      v
                          [OpenAI API (GPT & DALL-E)]
                                      |
                                      v
                            [Traveloka.com (Reference)]
```

## 6. Implementation Details

### 6.1 AI Model Configuration
- **Model**: GPT-4o-mini
- **Temperature**: 0.2 (for consistent outputs)
- **System Prompt**: Structured to generate specific vacation recommendations

### 6.2 Image Generation
- **Model**: DALL-E
- **Quality**: HD
- **Prompt Generation**: Uses a separate LLM chain to create detailed image prompts

### 6.3 Web Application
- **Route**: Single route ('/') handling both GET and POST requests
- **Data Flow**: User input -> AI processing -> Image generation -> Response rendering

### 6.4 Deployment
- Containerized using Docker for consistent environments
- Docker Compose used for easy deployment and scaling

## 7. User Flow

1. User accesses the web interface
2. User inputs vacation preferences or requirements
3. System processes input using the AI model
4. AI generates textual recommendations
5. System uses AI-generated content to create relevant images
6. Results are displayed to the user, including text recommendations and generated images
7. User can click on a link to proceed with bookings on Traveloka

## 8. Future Enhancements

1. **Personal Account Integration**: Allow users to connect their Google or other personal accounts for a more personalized experience.
2. **Direct Booking Capability**: Implement a payment gateway to enable users to make bookings directly through the application.
3. **Calendar Integration**: Connect with personal calendars to automatically sync vacation plans with the user's schedule.
4. **Expanded Travel Options**: Integrate with multiple travel platforms beyond Traveloka for more comprehensive options.
5. **User Feedback Loop**: Implement a system to collect and incorporate user feedback for continuous improvement of recommendations.

## 9. Challenges and Considerations

- Ensuring accuracy and relevance of AI-generated recommendations
- Maintaining user privacy and data security, especially with future personal account integrations
- Scaling the system to handle multiple users and requests efficiently
- Keeping the AI model up-to-date with current travel information and trends

## 10. Conclusion

The AI-Powered Vacation Planner Assistant PoC demonstrates the potential for AI to revolutionize travel planning. By leveraging advanced language models and image generation capabilities, it offers users a unique, personalized, and visually engaging way to plan their vacations. The current implementation provides a solid foundation for future enhancements and expansions in functionality.


# Getting Started
You can follow these steps to set up and run the project on your local machine.

## Installation
```
# Usage: Run in the terminal
----------------------------
## Clone the repository
git clone <repo_url>

## Set OpenAI API Key
export OPENAI_API_KEY=your_key
'or you can set in .env'

## Deploy using docker
docker-compose up --build
```

# The Result
Vacation Planner Assistant
![image](https://github.com/user-attachments/assets/6d7489f2-ae52-4135-ad8c-87ba849bea90)
![image](https://github.com/user-attachments/assets/7eef76fb-aaf0-47df-b638-e7065fcf2afc)
![image](https://github.com/user-attachments/assets/50982736-36c2-45bf-be66-5b1bed16bff9)
![image](https://github.com/user-attachments/assets/5a91279f-fc11-4c1c-a13b-e5ad740ddcf5)


