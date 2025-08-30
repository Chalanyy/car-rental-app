from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import re


@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').lower().strip()
        
        # Simple but smart responses
        ai_message = get_response(user_message)
        return JsonResponse({'message': ai_message})
    
    return render(request, 'chat/chat.html')

def get_response(message):
    """Simple but effective response system"""
    
    # Greetings
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
        return random.choice([
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! Nice to meet you!",
            "Greetings! How are you doing?"
        ])
    
    # How are you
    if any(phrase in message for phrase in ['how are you', 'how do you do', 'how are things']):
        return random.choice([
            "I'm doing great! How about you?",
            "I'm fine, thank you for asking!",
            "All good here! What about you?",
            "Fantastic! Thanks for asking!"
        ])
    
    # Name questions
    if any(phrase in message for phrase in ['your name', 'who are you', 'what are you']):
        return random.choice([
            "I'm your friendly chatbot assistant!",
            "You can call me ChatBot! I'm here to help.",
            "I'm an AI assistant built to chat with you!",
            "I'm your virtual assistant!"
        ])
    
    # Help requests
    if any(word in message for word in ['help', 'assist', 'support']):
        return random.choice([
            "I'd be happy to help! What do you need assistance with?",
            "Sure! I'm here to help. What can I do for you?",
            "Of course! How can I assist you today?",
            "I'm here to help! What would you like to know?"
        ])
    
    # Time questions
    if any(word in message for word in ['time', 'date', 'day']):
        return "I don't have access to real-time information, but you can check your system clock!"
    
    # Weather questions
    if any(word in message for word in ['weather', 'temperature', 'rain', 'sunny']):
        return "I can't check the weather right now, but you can look outside or check a weather app!"
    
    # Thanks
    if any(word in message for word in ['thank', 'thanks', 'appreciate']):
        return random.choice([
            "You're very welcome!",
            "Happy to help!",
            "No problem at all!",
            "My pleasure!",
            "Anytime!"
        ])
    
    # Goodbye
    if any(word in message for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return random.choice([
            "Goodbye! Have a wonderful day!",
            "See you later! Take care!",
            "Bye! It was nice chatting with you!",
            "Farewell! Come back anytime!"
        ])
    
    # Age questions
    if any(phrase in message for phrase in ['how old', 'your age', 'age are you']):
        return "I'm a timeless AI! I don't really have an age."
    
    # Favorite things
    if 'favorite' in message or 'favourite' in message:
        if 'color' in message:
            return "I like all colors! But blue is pretty nice - like the sky!"
        elif 'food' in message:
            return "I don't eat, but pizza sounds amazing!"
        else:
            return "I enjoy chatting with people like you!"
    
    # Questions about capabilities
    if any(phrase in message for phrase in ['what can you do', 'your abilities', 'can you']):
        return "I can chat with you, answer simple questions, and hopefully brighten your day!"
    
    # Default responses for unknown messages
    default_responses = [
        "That's interesting! Can you tell me more?",
        "I'm not sure I understand completely. Can you explain that differently?",
        "Hmm, that's something to think about!",
        "I'd love to learn more about that topic!",
        "That's a good point! What do you think about it?",
        "Interesting perspective! Can you elaborate?",
        "I'm still learning about that. What's your experience with it?",
        "That sounds important to you. Tell me more!",
        "I see! What made you think of that?",
        "Thanks for sharing that with me!"
    ]
    
    return random.choice(default_responses)