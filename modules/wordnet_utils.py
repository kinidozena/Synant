"""
WordNet utilities for the Telegram Synonym/Antonym Bot
"""
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import Synset
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import defaultdict
from .languages import get_message
import functools
import time
import nltk
import logging
import os
from pathlib import Path

# Configure logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'bot.log'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize WordNet
try:
    wordnet.ensure_loaded()
    logger.info("WordNet loaded successfully")
except LookupError:
    logger.info("Downloading WordNet data...")
    nltk.download('wordnet')
    logger.info("WordNet data downloaded successfully")
except Exception as e:
    logger.error(f"Error loading WordNet: {str(e)}")

# Cache for word lookups (expires after 1 hour)
word_cache = {}
CACHE_EXPIRY = 3600  # 1 hour in seconds

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
    
    # Just return the first definition and example to save processing time
    return synsets[0].definition(), synsets[0].examples()[0] if synsets[0].examples() else None

def get_word_info(word: str) -> Optional[Dict[str, Any]]:
    """Get synonyms and antonyms for a word using WordNet, including word types, meanings, and examples."""
    logger.info(f"Looking up word: {word}")
    
    # Check cache first
    current_time = time.time()
    if word in word_cache:
        cache_time, cache_data = word_cache[word]
        if current_time - cache_time < CACHE_EXPIRY:
            logger.info(f"Returning cached data for word: {word}")
            return cache_data

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
        synsets = wordnet.synsets(word)
        logger.info(f"Found {len(synsets)} synsets for word: {word}")
        
        for syn in synsets:
            pos = syn.pos()
            logger.info(f"Processing synset with POS: {pos}")
            
            # Get definition and examples for the word itself
            pos_data[pos]['meanings'].add(syn.definition())
            
            # Add up to 2 examples that contain the actual word
            example_count = 0
            for example in syn.examples():
                if word.lower() in example.lower() and example not in used_examples:
                    pos_data[pos]['examples'].add(example)
                    used_examples.add(example)
                    example_count += 1
                    if example_count >= 2:
                        break
            
            # Process each lemma in the synset (limit to first 10 lemmas)
            lemmas = list(syn.lemmas())[:10]
            logger.info(f"Processing {len(lemmas)} lemmas for synset")
            
            for lemma in lemmas:
                if lemma.name() != word:
                    # Get the best meaning and example for this synonym
                    meaning, example = find_best_synset_info(lemma.name(), pos)
                    if meaning:
                        syn_info = {
                            'word': lemma.name(),
                            'meaning': meaning,
                            'examples': []  # Skip examples for synonyms to improve performance
                        }
                        # Check if this synonym is already added
                        if not any(s['word'] == lemma.name() for s in pos_data[pos]['synonyms']):
                            pos_data[pos]['synonyms'].append(syn_info)
                
                # Process antonyms (but don't look for examples)
                antonyms = lemma.antonyms()
                logger.info(f"Found {len(antonyms)} antonyms for lemma: {lemma.name()}")
                
                for ant in antonyms:
                    try:
                        ant_info = {
                            'word': ant.name(),
                            'meaning': ant.synset().definition(),
                            'examples': []  # Skip examples for antonyms to improve performance
                        }
                        # Check if this antonym is already added
                        if not any(a['word'] == ant.name() for a in pos_data[pos]['antonyms']):
                            pos_data[pos]['antonyms'].append(ant_info)
                            logger.info(f"Added antonym: {ant.name()}")
                    except Exception as e:
                        logger.error(f"Error processing antonym {ant.name()}: {str(e)}")
        
        # Convert to final format
        result = {}
        for pos, data in pos_data.items():
            if data['synonyms'] or data['antonyms']:
                result[pos] = {
                    'pos_name': get_pos_name(pos),
                    'meanings': sorted(list(data['meanings'])),
                    'synonyms': data['synonyms'][:10],  # Limit to 10 synonyms
                    'antonyms': data['antonyms'],
                    'examples': sorted(list(data['examples']))[:2]  # Limit to 2 examples
                }
        
        # Cache the result
        if result:
            word_cache[word] = (current_time, result)
            logger.info(f"Cached result for word: {word}")
        else:
            logger.info(f"No results found for word: {word}")
            
        return result if result else None
    except Exception as e:
        logger.error(f"Error processing word {word}: {str(e)}")
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
        return get_message('word_not_found', lang).format(escape_markdown(word))
    
    response = []
    escaped_word = escape_markdown(word)
    
    # Sort POS by their readable names
    sorted_pos = sorted(info.keys(), key=lambda x: info[x]['pos_name'])
    
    # Check if there are any antonyms when in antonym mode
    if mode == 'antonym':
        has_antonyms = any(pos_data.get('antonyms') for pos_data in info.values())
        if not has_antonyms:
            return get_message('no_antonyms', lang).format(escaped_word)
    
    # Check if there are any synonyms when in synonym mode
    if mode == 'synonym':
        has_synonyms = any(pos_data.get('synonyms') for pos_data in info.values())
        if not has_synonyms:
            return get_message('no_synonyms', lang).format(escaped_word)
    
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
        
        # Add extra spacing between different parts of speech
        response.append("\n")
    
    return "\n".join(response) if response else get_message('no_results', lang).format(escaped_word) 