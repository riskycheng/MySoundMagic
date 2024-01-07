import re
import os


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


def refreshAvailableRolesList():
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    models_root_path = os.path.join(current_directory, "models")
    models_vits_root_path = os.path.join(models_root_path, "models_vits")
    models_vits2_root_path = os.path.join(models_root_path, "models_bert_vits2")
    model_vits_folders = os.listdir(models_vits_root_path)
    model_vits2_folders = os.listdir(models_vits2_root_path)

    # result map
    results = {}
    results["BERT_VITS2"] = {}
    for item in model_vits2_folders:
        roleName = item
        models = os.listdir(os.path.join(models_vits2_root_path, item))
        targetModel = None
        for m in models:
            if m.startswith('D_'):
                targetModel = m
                break
        results["BERT_VITS2"][roleName] = {'D_model': os.path.join(models_vits2_root_path, item, targetModel)}

    results["VITS"] = {}
    for item in model_vits_folders:
        roleName = item
        models = os.listdir(os.path.join(model_vits_folders, item))
        targetModel = None
        for m in models:
            if m.startswith('D_'):
                targetModel = m
                break
        results["VITS"][roleName] = {'D_model': os.path.join(model_vits_folders, item, targetModel)}

    return results


if "__main__" == __name__:
    res = refreshAvailableRolesList()
    print(res)
