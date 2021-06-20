import string
import re

with open("高中英语词汇3500词-TXT.txt") as word_file:
    word_raw = word_file.read()
word_raw_list = [line.strip() for line in word_raw.splitlines() if line.strip()]
print(len(word_raw_list))
word_list = []
prev_word = None
for line in word_raw_list:
    if "习惯用语和固定搭配" in line:
        break
    if line in string.ascii_uppercase:
        continue
    match = re.match(r"[a-zA-Z\-.\' ]+", line)
    word = match[0].strip()
    if not word:
        continue
    word_list.append(word)
    if any(letter not in string.ascii_letters for letter in word) or any(
        letter not in string.ascii_lowercase for letter in word[1:]
    ) or word[-1] == 'v':
        print(word)  # to check for anything weird
    if prev_word and word[0].lower() != prev_word[0].lower():
        print(f"{prev_word} -> {word}")
    prev_word = word
print(len(word_list))
word_set = set(word_list)
print(len(word_set))
print([word for word in word_set if word_list.count(word) > 1])
with open('words.txt', 'w') as plain_word_file:
    plain_word_file.write('\n'.join(sorted(word_set)))
