#import library
import speech_recognition as sr

def speech_to_text():
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("######################################## Talk ########################################")
        audio_text = r.listen(source,phrase_time_limit=5)
        print("######################################## Processing ##################################")
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print("Text :::  " + str(text))
            return text
        except:
            print("Sorry, I did not get that")

