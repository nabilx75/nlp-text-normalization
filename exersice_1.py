import re
text = "NLP Is Used In Many Applications."
print(text.lower())
#all capital letter became lowercase
#2
s = "Apple released a new iPhone; the apple I ate was sweet."
low = s.lower()
print(low)
print(low.split().count("apple"), "times the token 'apple'")
#in ner it becomes hared to distenguish between entities(ex:apple the company and the fruit)

#3
def is_alpha(text):
    w=re.findall(r"\b[A-Z]+\b", text)
    return bool(w)

def lower_text(text):
    result = []

    for word in text.split(" "):
        token = word.split("-")

        for i in range(len(token)):
            if not (is_alpha(token[i]) and (2 <= len(token[i].strip(".,!?")) or len(token[i].strip(".,!?")) <= 5)):
                token[i] = token[i].lower()

        result.append("-".join(token))

    return " ".join(result)


print(lower_text("The NLP course covers USA-based case studies."))


print(lower_text("yes, the NASA team said no to the idea."))
#q1:cuz for example in bag of words python and PYTHON are consider diff and the vocab get huge 
#q2: its importand cuz it make the vocab smaller and for ner it can make the diff between apple(fruit) and apple(the company)
