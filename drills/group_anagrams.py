def group_anagrams(words):
    groups = {}
    for w in words:
        sorted_letters = tuple((sorted(w)))
        if sorted_letters not in groups:
            groups[sorted_letters] = []
        groups[sorted_letters].append(w)
    return [group for group in groups.values() if len(group) >= 2]

print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))