import pyttsx3

def speak_insight(country, growth, inflation):

    engine = pyttsx3.init()

    text = f"""
    Executive insight.
    {country} shows export growth of {round(growth,2)} percent.
    Current inflation is {round(inflation,2)} percent.
    Strategic export opportunity detected.
    """

    engine.say(text)
    engine.runAndWait()