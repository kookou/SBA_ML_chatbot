from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

conversation = [
     "Hello",
     "Hi there!",
     "How are you doing?",
     "I'm doing great.",
     "That is good to hear",
     "Thank you.",
     "You're welcome.",
     "Hi, can I help you?",
     "Sure, I'd like to book a flight to Iceland.",
     "Your flight has been booked."
]

# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')
# Create a new Trainer
trainer = ListTrainer(chatbot)

trainer.train(conversation)
# Get a response to the input text 'Good morning.'
response = chatbot.get_response("Good morning!")
print(response)
# Get a response to the input text 'I would like to book a flight.'
response = chatbot.get_response('I would like to book a flight.')
print(response)