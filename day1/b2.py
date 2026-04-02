# 🔹 Bài 2: Group Anagrams

# Yêu cầu:
# Cho list string, nhóm các từ là anagram lại với nhau.
from collections import defaultdict

def groupAnagrams(strs):
    d = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        d[key].append(s)
    return list(d.values())

print(groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))