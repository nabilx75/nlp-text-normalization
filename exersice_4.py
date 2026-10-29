import re
url = r"https?://[^\s]+[^\s.,;:!?)]"
email = r"[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"
def clean_text(text):
 text = text.lower() 
 text = re.sub(url, " <URL> ", text)
 text = re.sub(email, " <EMAIL> ", text)
 text = re.sub(r"([a-z])\1{2,}", r"\1\1", text)#------------------------------------------------------------------------------------------
 text = re.sub(r"\s+", " ", text).strip()
 return text

#2
t = ("OMG this courseeee is SOOOO good!!! 10/10 would recommend :) Visit https://univ.dz/nlp for more info. Contact: prof@univ.dz")
cleaned = clean_text(t)
print("BEFORE:", t)
print("AFTER :", cleaned)

#3
from nltk.tokenize import word_tokenize
tok_before = word_tokenize(t)
tok_after = word_tokenize(cleaned)
print(len(tok_before), "tokens,", len(set(tok_before)), "distinct before")
print(len(tok_after), "tokens,", len(set(tok_after)), "distinct after")
