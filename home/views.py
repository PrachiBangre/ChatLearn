import json
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import SignUp, SignIn
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from nltk.corpus import wordnet
import random
import pyttsx3
from textblob import WordList

def index(request):
    return render(request, 'home/index.html')

def feedback(request):
    return render(request, 'home/feedback.html')

def about(request):
    return render(request, 'home/about.html')

def signup(request,*args,**kwargs):
    
    print(request.method)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        highest_education = request.POST.get('education')
        reason_to_learn = request.POST.get('reason')
        current_language_level = request.POST.get('language_level')
        
        if SignUp.objects.filter(email=email).exists():
            messages.warning(request, "User with that name already exists.")
            return HttpResponseRedirect(request.path_info)
        
        else:
            user_obj = SignUp.objects.create(
                full_name=full_name,
                email=email,
                password=password,
                gender=gender,
                education=highest_education,
                reason_to_learn=reason_to_learn,
                language_level=current_language_level
            )
            print('success')
            user_obj.save()
            
            # Redirect to a success page or login page
            return redirect('/')

    return render(request, 'home/signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Signed In.')
            return redirect('/index/')  # Replace 'home' with the name of your home page URL
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'home/signin.html')

##########################################################################
def services(request):
    return render(request, 'home/services.html')


#####################################
# views.py
from django.shortcuts import render
from django.http import JsonResponse
import random
import pyttsx3
from nltk.corpus import wordnet

# Define your word-related functions here
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_meaning(word):
    meaning = wordnet.synsets(word)
    if meaning:
        return meaning[0].definition()
    else:
        return "No meaning found."

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def get_antonyms(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
    return antonyms

def get_related_words(word):
    related_words = set()
    for synset in wordnet.synsets(word):
        related_words.update(lemma.name() for lemma in synset.lemmas())
    return list(related_words)

def get_hypernyms(word):
    hypernyms = set()
    for synset in wordnet.synsets(word):
        for hypernym in synset.hypernyms():
            hypernyms.update(hypernym.lemma_names())
    return hypernyms

def get_random_word():
    words = list(wordnet.words())
    return random.choice(words)

def get_word_examples(word):
    examples = []
    for synset in wordnet.synsets(word):
        examples.extend(synset.examples())
    return examples


def chatbot(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        word = request.POST.get('word')

        if choice == '1':
            speak(word)
            message = f"Pronouncing {word}"
        elif choice == '2':
            meaning = get_meaning(word)
            message = meaning
        elif choice == '3':
            synonyms = get_synonyms(word)
            message = f"Synonyms of '{word}': {', '.join(synonyms)}"
        elif choice == '4':
            antonyms = get_antonyms(word)
            message = f"Antonyms of '{word}': {', '.join(antonyms)}"
        elif choice == '5':
            random_word = get_random_word()
            message = f"Random word: {random_word}"
        elif choice == '6':
            examples = get_word_examples(word)
            message = f"Examples of '{word}':\n- {'\n- '.join(examples)}"
        elif choice == '7':
            related_words = get_related_words(word)
            message = f"Related words of '{word}': {', '.join(related_words)}"
        elif choice == '8':
            hypernyms = get_hypernyms(word)
            message = f"Hypernyms of '{word}': {', '.join(hypernyms)}"
        elif choice == '9':
            message = "Goodbye!"
        else:
            message = "Invalid choice. Please try again."

        return render(request, 'home/chatbot.html', {'message': message})
    return render(request, 'home/chatbot.html', {'message': "Invalid Request"})

##############################################################################################################
from django.shortcuts import render
from textblob import Word
import pyttsx3

def pronounce_word(word):
    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()
    engine.setProperty('volume', 9.0)
    return True  # Indicate the word was pronounced successfully

class SpellChecker:
    def __init__(self, text):
        self.word = Word(text)

    def correct_spelling(self):
        temp_list = self.word.spellcheck()
        suggestions = [i[0] for i in temp_list]
        return suggestions

def checker(request):
    word = request.POST.get('word', '')  # Get the word submitted via the form

    if request.method == 'POST':
        spell_checker = SpellChecker(word)
        suggestions = spell_checker.correct_spelling()
        pronounced = pronounce_word(word)
        return render(request, 'home/checker.html', {'word': word, 'suggestions': suggestions, 'pronounced': pronounced})
    else:
        return render(request, 'home/checker.html', {'word': ''})  # Render the form with an empty word initially

##################################################################

def quiz(request):
    return render(request, 'home/quiz.html')
###########################################################

# views.py

from django.shortcuts import render
from nltk.corpus import wordnet
import random

# Function to retrieve a random word from WordNet
def get_random_word():
    # Get all synsets
    synsets = list(wordnet.all_synsets())
    # Pick a random synset
    random_synset = random.choice(synsets)
    # Get the name of the first lemma in the synset
    random_word = random_synset.lemmas()[0].name()
    return random_word

# Function to update the Word of the Day
def update_word_of_the_day():
    word_of_the_day = get_random_word()

    # Get the definition of the word
    synsets = wordnet.synsets(word_of_the_day)
    if synsets:
        # Use the first synset to get the definition
        definition = synsets[0].definition()
    else:
        definition = "Definition not found."

    # Return the word and its definition
    return {'word': word_of_the_day, 'definition': definition}

# View function for rendering the word template
def word(request):
    word_data = update_word_of_the_day()
    return render(request, 'home/word.html', word_data)



############################################################
def synonyms_antonyms(request):
    return render(request, 'home/synonyms_antonyms.html')