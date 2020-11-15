import re

# populate with results
# needs optimizations for larger lists
collection = ["test", "nice", "migarov", "migasch", "mig"]


def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = ".*?".join(user_input)
    regex = re.compile(pattern)
    for item in collection:
        match = regex.search(item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]
