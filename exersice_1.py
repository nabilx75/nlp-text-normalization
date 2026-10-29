import re
text = "NLP Is Used In Many Applications."
print(text.lower())

#2
s = "Apple released a new iPhone; the apple I ate was sweet."
low = s.lower()
print(low)
print(low.split().count("apple"), "times the token 'apple'")


#3

def smart_lower(text):
    result = []

    for word in text.split():
        parts = word.split("-")

        for i in range(len(parts)):
            if not (parts[i].isupper() and 2 <= len(parts[i].strip(".,!?")) <= 5):
                parts[i] = parts[i].lower()

        result.append("-".join(parts))

    return " ".join(result)


print(smart_lower("The NLP course covers USA-based case studies."))


