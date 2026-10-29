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
def normalize_numbers_generic(text):
    return re.sub(NUMBER, "<NUM>", text)

def normalize_numbers_magnitude(text):
    def repl(match):
        value = float(match.group().replace(",", ""))
        return "<NUM_SMALL>" if value < 100 else "<NUM_LARGE>"

    return re.sub(NUMBER, repl, text)

print(normalize_numbers_generic(invoice))
print(normalize_numbers_magnitude(invoice))