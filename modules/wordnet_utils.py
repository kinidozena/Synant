"""
WordNet utilities for the Telegram Synonym/Antonym Bot
"""
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import Synset
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import defaultdict
from .languages import get_message

def escape_markdown(text: str) -> str:
    """Escape Markdown special characters."""
    special_chars = ['_', '*', '`', '[', ']']
    for char in special_chars:
        text = text.replace(char, '\\' + char)
    return text

def get_pos_name(pos: str) -> str:
    """Convert WordNet POS tag to readable name."""
    pos_names = {
        'n': 'Noun',
        'v': 'Verb',
        'a': 'Adjective',
        'r': 'Adverb',
        's': 'Adjective Satellite'
    }
    return pos_names.get(pos, 'Other')

def find_matching_example(word: str, synsets: List[Synset]) -> Optional[str]:
    """Find an example sentence that actually contains the word."""
    word_forms = {word, word.replace('_', ' ')}  # Include both forms for multi-word terms
    
    # First try to find an example containing the exact word
    for syn in synsets:
        for example in syn.examples():
            example_lower = example.lower()
            if any(form.lower() in example_lower for form in word_forms):
                return example
    
    # If no matching example found, return None
    return None

def find_best_synset_info(word: str, pos: str) -> Tuple[Optional[str], Optional[str]]:
    """Find the most relevant definition and example for a word in a specific part of speech."""
    synsets = wordnet.synsets(word, pos=pos)
    if not synsets:
        return None, None
    
    # Try to find an example that contains the actual word
    example = find_matching_example(word, synsets)
    
    # Use the definition from the same synset as the matching example if found
    if example:
        for syn in synsets:
            if example in syn.examples():
                return syn.definition(), example
    
    # If no matching example found, just return the first definition
    return synsets[0].definition(), None

def get_word_info(word: str) -> Optional[Dict[str, Any]]:
    """Get synonyms and antonyms for a word using WordNet, including word types, meanings, and examples."""
    try:
        # Dictionary to store words by POS
        pos_data = defaultdict(lambda: {
            'meanings': set(),
            'synonyms': [],  # List of dicts with word, meaning, examples
            'antonyms': [],  # List of dicts with word, meaning, examples
            'examples': set()
        })
        
        # Keep track of used examples to avoid repetition
        used_examples = set()
        
        # First, collect all synsets for the input word
        for syn in wordnet.synsets(word):
            pos = syn.pos()
            
            # Get definition and examples for the word itself
            pos_data[pos]['meanings'].add(syn.definition())
            
            # Find examples that contain the actual word
            for example in syn.examples():
                if word.lower() in example.lower() and example not in used_examples:
                    pos_data[pos]['examples'].add(example)
                    used_examples.add(example)
            
            # Process each lemma in the synset
            for lemma in syn.lemmas():
                if lemma.name() != word:
                    # Get the best meaning and example for this synonym
                    meaning, example = find_best_synset_info(lemma.name(), pos)
                    if meaning:
                        # Only use the example if it's not already used and contains the word
                        if example and example not in used_examples:
                            used_examples.add(example)
                        else:
                            example = None
                            
                        syn_info = {
                            'word': lemma.name(),
                            'meaning': meaning,
                            'examples': [example] if example else []
                        }
                        # Check if this synonym is already added
                        if not any(s['word'] == lemma.name() for s in pos_data[pos]['synonyms']):
                            pos_data[pos]['synonyms'].append(syn_info)
                
                # Process antonyms
                for ant in lemma.antonyms():
                    # Get the best meaning and example for this antonym
                    meaning, example = find_best_synset_info(ant.name(), pos)
                    if meaning:
                        # Only use the example if it's not already used and contains the word
                        if example and example not in used_examples:
                            used_examples.add(example)
                        else:
                            example = None
                            
                        ant_info = {
                            'word': ant.name(),
                            'meaning': meaning,
                            'examples': [example] if example else []
                        }
                        # Check if this antonym is already added
                        if not any(a['word'] == ant.name() for a in pos_data[pos]['antonyms']):
                            pos_data[pos]['antonyms'].append(ant_info)
        
        # Convert to final format
        result = {}
        for pos, data in pos_data.items():
            if data['synonyms'] or data['antonyms']:
                result[pos] = {
                    'pos_name': get_pos_name(pos),
                    'meanings': sorted(list(data['meanings'])),
                    'synonyms': data['synonyms'][:10],  # Limit to 10 synonyms
                    'antonyms': data['antonyms'],
                    'examples': sorted(list(data['examples']))[:3]  # Limit to 3 examples
                }
        
        return result if result else None
    except Exception as e:
        return None

def get_number_emoji(n: int) -> str:
    """Convert a number to its emoji representation."""
    number_emojis = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟"
    }
    return number_emojis.get(n, str(n))

def format_word_info(word: str, info: Optional[Dict[str, Any]], mode: str, lang: str) -> str:
    """Format word information for display with proper markdown and language support."""
    if info is None:
        return get_message('no_results', lang).format(escape_markdown(word))
    
    response = []
    escaped_word = escape_markdown(word)
    
    # Sort POS by their readable names
    sorted_pos = sorted(info.keys(), key=lambda x: info[x]['pos_name'])
    
    for i, pos in enumerate(sorted_pos, 1):
        pos_data = info[pos]
        pos_name = pos_data['pos_name']
        
        # Word type section with meaning
        response.append(f"\n{get_number_emoji(i)} {escaped_word} as *{pos_name}*:")
        if pos_data['meanings']:
            response.append(f"Meaning: {escape_markdown(pos_data['meanings'][0])}")
        
        # Add main example if available
        if pos_data['examples']:
            response.append(f"Example:")
            response.append(f"{escape_markdown(pos_data['examples'][0])}\n")
        
        # Synonyms section
        if mode in ['synonym', 'both'] and pos_data['synonyms']:
            response.append(f"\n📚 Synonyms for *{pos_name.lower()}* '{escaped_word}'\n")
            for syn in pos_data['synonyms']:
                response.append(f"• {escape_markdown(syn['word'])}")
                response.append(f"Meaning: {escape_markdown(syn['meaning'])}")
                if syn['examples']:
                    response.append(f"Example: {escape_markdown(syn['examples'][0])}")
                response.append("")  # Empty line between synonyms
        
        # Antonyms section
        if mode in ['antonym', 'both'] and pos_data['antonyms']:
            if mode == 'both':
                response.append("\n")  # Extra line for separation
            response.append(f"\n⚡️ Antonyms for *{pos_name.lower()}* '{escaped_word}'\n")
            for ant in pos_data['antonyms']:
                response.append(f"• {escape_markdown(ant['word'])}")
                response.append(f"Meaning: {escape_markdown(ant['meaning'])}")
                if ant['examples']:
                    response.append(f"Example: {escape_markdown(ant['examples'][0])}")
                response.append("")  # Empty line between antonyms
        
        if not pos_data['synonyms'] and mode == 'synonym':
            response.append(get_message('no_synonyms', lang))
        if not pos_data['antonyms'] and mode == 'antonym':
            response.append(get_message('no_antonyms', lang))
        
        # Add extra spacing between different parts of speech
        response.append("\n")
    
    return "\n".join(response) 