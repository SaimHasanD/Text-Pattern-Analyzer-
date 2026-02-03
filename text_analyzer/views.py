from django.shortcuts import render
from collections import Counter

def reading_time_view(request):
    minutes = None
    seconds = None
    user_text = ""
    
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
    
        cleaned_words = []
        for word in words:
            clean_word = word.lower().strip('.,!?";:()[]{}')        
            if clean_word:
                cleaned_words.append(clean_word)
        
        word_counts = Counter(cleaned_words)
        top_words = word_counts.most_common(3)



    context = {
        'minutes': minutes,
        'seconds': seconds,
        'user_text': user_text,
        'top_words': top_words,
    }
    
    return render(request, 'text_analyzer/reading_time.html', context)