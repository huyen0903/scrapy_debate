from deep_translator import GoogleTranslator

# Use any translator you like, in this example GoogleTranslator
translated = GoogleTranslator(source='auto', target='vi').translate("This House would make all museums free of charge")
print(translated)