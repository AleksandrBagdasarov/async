a = ['11', '22', '33 3', '4\n4', ' ', '\n', '', '']



def text_cleaner(full_text: list) -> str:
    clean_text = [clean(text) for text in full_text if clean(text)]
    return '\n***\n'.join(clean_text)

def clean(text: str) -> str:
    return text.replace(' ', '').replace('\t', '').replace('\n', '')


print(text_cleaner(a))