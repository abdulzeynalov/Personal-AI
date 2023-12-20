from datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
activationWord = 'computer'

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

appId = 'KAE5H3-JG66PG9V7X'
wolframClient = wolframalpha.Client(appId)

def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')
    
    with sr.Microphone() as source:
        listener.pause_thershold = 2
        input_speech = listener.listen(source)

    try:
        print('recognizing speech....')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'the input speech was: {query}')
    except Exception as exception:
        print("I did not quite catch that")
        speak('I did not quite catch that')
        print(exception)
        return 'none'
    
    return query

def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('no wikipedia result')
        return 'no result received'
    try:
        wikipage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikipage = wikipedia.page(error.option[0])
    print(wikipage.title)
    wikiSummary = str(wikipage.summary)
    return wikiSummary

def listOrdict(var):
    if isinstance(var, list):
        return var[0]['plaintext']

def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)
    
    if response['@success'] == 'false':
        return 'could not computer'
    
    else:
        result = ''
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]

        if (('result') in pod1['@Qtitle'].lower()) or (pod1.get('@primary','false') == 'true') or ('definition' in pod1['@title'].lower):
            
            result = listOrdict(pod1['subpod'])
            
            return result.split('(')[0]
        else:
            question = listOrdict(pod0['subpod'])
            return question.split('(')[0]
            speak('computation failed. quering universal databank.')
            return search_wikipedia(question)



#main loop
if __name__ == '__main__':
    speak("all systems nominal")

    while True:
        query =  parseCommand().lower().split()
        
        if query[0] == activationWord:
            query.pop(0)


            if query[0] == 'say':
                if 'hello' in query:
                    speak('greetings, all.')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)

        if query[0] == 'go' and query[1] == 'to':
            speak('Opening...')
            query = ' '.join(query[2:])
            webbrowser.get('chrome').open_new(query)

        if query[0] == 'wikipedia':
            query = ' '.join(query[1:])
            speak('querying the universal databank.')
            speak(search_wikipedia(query))
        
        if query[0] == 'compute' or query  [0] == 'computer':
            query = ' '.join(query[1:])
            speak('computing')
            try:
                result = search_wolframAlpha(query)
                speak(result)
            except:
                speak("unable to compute.")