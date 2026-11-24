def is_anagram(s, t):
    s = s.lower().replace(" ", "")
    t = t.lower().replace(" ", "")
    if len(s) != len(t):
        return False
    s_counts = {}
    t_counts = {}
    for ch in s:
        s_counts[ch] = s_counts.get(ch, 0) + 1
    for ch in t:
        t_counts[ch] = t_counts.get(ch, 0) + 1
    if s_counts == t_counts:
        return True
    return False

print(is_anagram("listen", "silent"))