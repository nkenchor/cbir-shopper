
from app.application.services.retrieval_services import google_vector_loader


  
def get_suggestions(word, topn=10):
   
    model = google_vector_loader.LOADED_MODEL
    try:
        # First, try to get synonyms for the word/phrase as a whole
        return [item[0].lower() for item in model.similar_by_word(word, topn=topn)]
    except KeyError:
        # If the word/phrase isn't in the model's vocabulary,
        # split it and try to get synonyms for individual words
        words = word.split()
        if len(words) == 1:
            return []  # the word isn't in the vocabulary and isn't a phrase
        
        synonyms = []
        for w in words:
            try:
                synonyms.extend([item[0].lower() for item in model.similar_by_word(w, topn=topn)])
            except KeyError:
                pass  # this word isn't in the vocabulary
        
        # Add the original split words back into the list
        synonyms.extend([w.lower() for w in words])
        
        # Deduplicate and limit to topn results
        return list(set(synonyms))[:topn]
