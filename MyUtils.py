import re


def split_long_sentences(long_sentences):
    # Define common symbols for splitting
    common_symbols = r'[.!?]'
    # Special symbol for splitting
    special_symbol = r'\[\|\]'
    # Chinese punctuation marks
    chinese_punctuation = r'[。，]'

    # Combine common symbols, special symbol, and Chinese punctuation into a single regex pattern
    split_pattern = f'{common_symbols}|{special_symbol}|{chinese_punctuation}'

    # Use re.split() to split the long sentences based on the pattern
    split_sentences = re.split(split_pattern, long_sentences)

    # Remove empty strings from the result
    split_sentences = [item.strip() for item in split_sentences if item.strip()]

    return split_sentences
