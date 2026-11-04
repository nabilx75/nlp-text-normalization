import re
text = "The course lasts 20 hours and contains 12 exercises."
result = re.sub(r"\d+", "<NUM>", text)
print(result)

invoice = "The invoice #4521 totals $1,250.00, due in 30 days."
print(re.sub(r"\d+", "<NUM>", invoice))

#2
NUMBER=r"\d+(?:,\d{3})*(?:\.\d+)?"
print(re.sub(NUMBER,"<NUM>", invoice))

#3
def normalize_numbers_1st_version(text):
    
    return re.sub(NUMBER, "<NUM>", text)


def normalize_numbers_2nd_version(text):
    NUMBER = r"\d+(?:,\d{3})*(?:\.\d+)?"
    cleaned_text = re.sub(r"(?<=\d),(?=\d)", "", text)
    numbers=re.findall(NUMBER, cleaned_text )
    for n in numbers:
        if float(n) > 100:
           cleaned_text=re.sub(n, "<NUM_LARGE>", cleaned_text )
        else:
              cleaned_text=re.sub(n, "<NUM_small>", cleaned_text )
        # if float(n) > 100:
        #     cleaned_text = cleaned_text.replace(n, "<NUM_LARGE>", 1)
        # else:
        #     cleaned_text = cleaned_text.replace(n, "<NUM_SMALL>", 1)  
    

    return cleaned_text


print(normalize_numbers_1st_version(invoice))
print(normalize_numbers_2nd_version(invoice))


#q1:no one is enough to compare invoice amounts but at least the second one it tells if the number is big or not 
#q2:Replace numbers with a placeholder when the exact value does not matter and it reduces the vocabulary
#Keep numbers as they are when the exact values carry the meaning for example financial documents scientific results