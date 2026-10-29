import re
text = "NLP is very useful."
print(re.sub(r"\s+", " ", text).strip())

messy = "NLP\tis\n\nvery\u00a0\u00a0useful."
print(messy)
print("-------------------------------")
cleaned = re.sub(r"\s+", " ", messy).strip()
print(cleaned)


#2
print(bool(re.match(r"\s", "\u00a0"))) 
print(bool(re.match(r"\s", "\u00a0", re.ASCII)))
print(re.sub(r"\s+", " ", "a\u200bb"))

#3


def normalize_whitespace(text):
 text = text.replace("\u00a0", " ").replace("\u200b", "") # special spaces
 lines = [line.strip() for line in text.splitlines()] # strip every line
 text = " ".join(line for line in lines if line) # join, skip empty lines
 return re.sub(r"\s+", " ", text).strip() # collapse what is left

#4
paragraph = """ Natural language processing is a field of AI\u00a0\u00a0that studies \t how computers understand text. """
print(paragraph)
print(normalize_whitespace(paragraph))