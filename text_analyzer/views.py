from django.shortcuts import render
from collections import Counter
import re
import nltk

def reading_time_view(request):
    minutes = None
    seconds = None
    user_text = ""
    top_words = []
    top_phrases = []
    most_complex_sentence = None
    most_simple_sentence = None
    complex_score = None
    simple_score = None

    
    if request.method == 'POST':
        user_text = request.POST.get('user_text', '')
        
        # Split text
        words = user_text.split()
        total_words = len(words)
        
        # Calculate reading time
        read_time = total_words / 200
        
        # Separate minutes and seconds
        minutes = int(read_time) 
        seconds = int((read_time - minutes) * 60) 
    
    #Find top 3 most repeated single words
        cleaned_words = []
        for word in words:
            clean_word = word.lower().strip('.,!?";:()[]{}')        
            if clean_word:
                cleaned_words.append(clean_word)
        
        word_counts = Counter(cleaned_words)
        top_words = word_counts.most_common(3)

    #Find top 3 most repeated 2-word phrases
        two_word_phrases = []
        for i in range(len(cleaned_words) - 1):  
            phrase = cleaned_words[i] + " " + cleaned_words[i + 1]
            two_word_phrases.append(phrase)

        phrase_counts = Counter(two_word_phrases)
        
        top_phrases = phrase_counts.most_common(3)

        # Split text into sentences using NLTK
        sentences = nltk.sent_tokenize(user_text)
        
        connectors = {'and', 'but', 'because', 'although', 'which', 'that', 'while',
                      'however', 'therefore', 'if', 'when', 'since', 'though'}
        
        sentence_scores = []

        for sentence in sentences:
            # Clean the sentence
            sentence_words = sentence.split()
            
            if len(sentence_words) == 0:
                continue
            
            score = 0
            long_words = 0
            connector_count = 0
            punctuation_count = 0
            for char in sentence:
                if char in '.,!?";:()[]{}':
                    punctuation_count += 1

            for i, word in enumerate(sentence_words):
                clean_word = word.lower().strip('.,!?";:()[]{}')
                
                if len(clean_word) > 8:
                    long_words += 1
                
                if clean_word in connectors:
                    connector_count += 1

            score += min(long_words, 3)
            score += min(connector_count, 4)
            score += min(punctuation_count, 2)
                           
            # Calculate complexity score
            # score = long_words + connector_count + punctuation_count
            word_count = len(sentence_words)
            if word_count >= 30:
                score += 5
            elif word_count >= 21:
                score += 3
            elif word_count >= 10:
                score += 1

            sentence_scores.append({
                'text': sentence,
                'score': score
            })

        # Find most complex and most simple sentences
        if sentence_scores:
            sorted_sentences = sorted(sentence_scores, key=lambda x: x['score'])

            most_simple = sorted_sentences[0]
            most_complex = sorted_sentences[-1]

            most_complex_sentence = most_complex['text']
            complex_score = most_complex['score']

            most_simple_sentence = most_simple['text']
            simple_score = most_simple['score']

    context = {
        'minutes': minutes,
        'seconds': seconds,
        'user_text': user_text,
        'top_words': top_words,
        'top_phrases': top_phrases,
        'most_complex_sentence': most_complex_sentence,
        'most_simple_sentence': most_simple_sentence,
        'complex_score': complex_score,
        'simple_score': simple_score,
    }
    
    return render(request, 'text_analyzer/reading_time.html', context)