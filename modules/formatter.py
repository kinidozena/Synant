"""
Response formatting module
"""
import logging
from typing import Dict, Any, List
from modules.translations import get_text

logger = logging.getLogger(__name__)


def format_response(
        word_info: Dict[str, Any],
        request_type: str,
        language: str,
        is_corrected: bool = False,
        corrected_word: str = None
) -> str:
    """
    Format the response message based on the word information.

    Args:
        word_info: Dictionary containing word information
        request_type: 'synonyms', 'antonyms', or 'both'
        language: User's preferred language
        is_corrected: Whether the word was corrected for spelling
        corrected_word: The corrected word if applicable

    Returns:
        Formatted response string
    """
    word = word_info["word"]
    response_parts = []

    # Add spelling correction message if applicable
    if is_corrected:
        response_parts.append(f"*{get_text('spelling_corrected', language)}:* '{corrected_word}'")

    # Add word header
    response_parts.append(f"*{word.upper()}*")

    # Add definition
    if word_info["definitions"]:
        response_parts.append(f"\n*{get_text('definition', language)}:*")
        for i, def_item in enumerate(word_info["definitions"][:3], 1):  # Limit to 3 definitions
            pos = def_item.get("part_of_speech", "")
            definition = def_item.get("definition", "")
            pos_text = f" ({pos})" if pos else ""
            response_parts.append(f"{i}. {definition}{pos_text}")

    # Add synonyms if requested
    if request_type in ['synonyms', 'both'] and word_info["synonyms"]:
        response_parts.append(f"\n*{get_text('synonyms', language)}:*")
        synonyms_list = []
        for i, synonym in enumerate(word_info["synonyms"][:10], 1):  # Limit to 10 synonyms
            synonyms_list.append(f"{i}. {synonym}")
        response_parts.append("\n".join(synonyms_list))

    # Add antonyms if requested
    if request_type in ['antonyms', 'both'] and word_info["antonyms"]:
        response_parts.append(f"\n*{get_text('antonyms', language)}:*")
        antonyms_list = []
        for i, antonym in enumerate(word_info["antonyms"][:10], 1):  # Limit to 10 antonyms
            antonyms_list.append(f"{i}. {antonym}")
        response_parts.append("\n".join(antonyms_list))

    # Add examples
    if word_info["examples"]:
        response_parts.append(f"\n*{get_text('examples', language)}:*")
        examples_list = []
        for i, example in enumerate(word_info["examples"][:3], 1):  # Limit to 3 examples
            examples_list.append(f"{i}. _{example}_")
        response_parts.append("\n".join(examples_list))

    # Combine all parts
    return "\n".join(response_parts)
