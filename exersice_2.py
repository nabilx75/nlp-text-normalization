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
#in modern Python \s does match \u00a0 but some older tools or custom code may not
#3


def normalize_whitespace(text):
 text = text.replace("\u00a0", " ").replace("\u200b", "") #spaces
 lines = [line.strip() for line in text.splitlines()] #strip lines
 text = " ".join(line for line in lines if line) # join
 return re.sub(r"\s+", " ", text).strip() # #clean inside lines

#4
paragraph = """ Natural language processing is a field of AI\u00a0\u00a0that studies \t how computers understand text. """
print(paragraph)
print(normalize_whitespace(paragraph))

#q1: remove diff spaces breaks
#q2:Real text messy because websites PDF people leave behind extra spaces, and invisible sticky notes(pictures and some rules in apps)
#q3: we cant remove all the spaces because then for example when extracting sb info the name adress etc all get merged also in code the space matters