import os
import unicodedata

from devanagari_functions import *

devanagariDoubleDanda = '\u0965'
devanagariDanda = '\u0964'
hyphen = '\u002D'


###############################################################################
# READ DOCUMENTS (examples)
###############################################################################

# FULL

# File without extras; only with the shlokas, and "__ uvaaca"
fileName = os.path.join(rootDir, 'docs/BG-clean.txt')

# Read all characters
BG = read_unicode_file(fileName)

# Replace with numbers
yIdx = unicode_file_to_idx_sequences(BG, pad=True, padding='post',
                                        maxlen=maxlen)


# CHAPTER 01

# File without extras; only with the shlokas, and "__ uvaaca"
fileName = os.path.join(rootDir, 'docs/BG-clean-C01.txt')

# Read file
fileLines01 = read_unicode_file(fileName)

# Replace with numbers
yIdx01 = unicode_file_to_idx_sequences(fileLines01, pad=True, padding='post',
                                        maxlen=maxlen)


###############################################################################
# CLEAN FILE
###############################################################################

# File without extras:
# only with the shlokas (including "__ uvaaca"), shloka numbers
fileName = os.path.join(rootDir, 'docs/BG-edited.txt')

# Read file
fileLines = read_unicode_file(fileName)

# Remove blank lines
fileLines = list(filter(('').__ne__, fileLines))

# Remove leading spaces, etc.
for i, line in enumerate(fileLines):
    # Remove leading spaces
    fileLines[i] = fileLines[i].lstrip()
    # Remove single dandas at the end of line
    fileLines[i] = fileLines[i].split(devanagariDanda)[0].rstrip()
    # Remove double dandas at the end of line, and the line numbers
    fileLines[i] = fileLines[i].split(devanagariDoubleDanda)[0].rstrip()

# Again remove blank lines
fileLines = list(filter(('').__ne__, fileLines))

# Add stop character after every line
for i, line in enumerate(fileLines):
    fileLines[i] += devanagariDanda

# Write clean file
fileName = os.path.join(rootDir, 'docs/BG-clean.txt')
write_unicode_file(fileName, fileLines)


###############################################################################
# FIND MAXLEN OF SHLOK CHARACTER LINES
###############################################################################

# Find maxlen
maxlen = 0
for line in fileLines:
    if len(line) > maxlen:
        maxlen = len(line)

# maxlen = 56
print("maxlen =", maxlen)


###############################################################################
# SPLIT SHLOKAS INTO SYLLABLE (guru and laghu)
###############################################################################

# RUN

# Read shlokas
fileName = os.path.join(rootDir, 'docs/BG-clean.txt')
BG = read_unicode_file(fileName)

# Make shlokasSyllables, allSyllables for shlokasLines
shlokasSyllables, allSyllables = shlokas_to_syllables(BG)

# Find all unique syllables, and frequency
uniqueSyllables = set(allSyllables)
uniqueSyllablesCount = {syllable:allSyllables.count(syllable) for syllable in uniqueSyllables}

# Find all shlokLengths
shlokLengths = shlok_lengths(shlokasSyllables)

# Save shlokLengths and indices
np.save(os.path.join(rootDir, "docs/shlokLengths.npy"), shlokLengths)

# Read shlokLengths
shlokLengths = np.load(os.path.join(rootDir, "docs/shlokLengths.npy")).item()

# Find number of shlokas of each length
for key in sorted(shlokLengths.keys()):
    print(key, len(shlokLengths[key]))
# 11 215
# 12 5 : [118, 119, 177, 710, 1303]
# 16 1291
# 17 1 : ?????????????????????????????? ???????????? ?????????????????????????????????????????????????????????????????? ??? ??????-??????(1)

# Make binary syllables
shlokasBinarySyllables = binarize_shlokas_syllables(shlokasSyllables)

# Check anushtubh chandas
# 5th, 6th of first & third padas are like '01'
# shlokasBinarySyllables[s][4] = 0, shlokasBinarySyllables[s][5] = 1
# 5th, 6th, 7th of second & fourth padas are like '010'
# shlokasBinarySyllables[s][12] = 0, shlokasBinarySyllables[s][13] = 1, shlokasBinarySyllables[s][14] = 0
for s, shlok in enumerate(shlokasSyllables):
    if len(shlok) == 16:
        if shlokasBinarySyllables[s][4] != 0 or shlokasBinarySyllables[s][5] != 1 \
                or shlokasBinarySyllables[s][12] != 0 or shlokasBinarySyllables[s][13] != 1 \
                or shlokasBinarySyllables[s][14] != 0:
            print(s)
            print(shlok)
            print(shlokasSyllables[s])
            print(shlokasBinarySyllables[s])
            break


###############################################################################
# CHARACTERS ANALYSIS
###############################################################################

# # Find unicode name
# [unicodedata.name(c) for c in fileText[:10]]

# Find the categories spanned by all Devanagari characters
categories = []
chars = []
for c in range(0x7F):
    charNum = 0x0900 + c
    categories.append(unicodedata.category(chr(charNum)))
    if categories[-1] == 'Mc':
        chars.append(chr(charNum))

# Find the unique set of categories
categories = set(categories)

# Find all char names in one category
for c in chars:
    unicodedata.name(c)

# >>> categories
# {'Nd', 'Lo', 'Mn', 'Po', 'Lm', 'Mc'}
# Nd = Number, decimal digit : ???, ???, ???, ???, ???, ???, ???, ???, ???, ???
# Lo = Letter, other:
# ['???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???',
# '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???',
# '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???',
# '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???',
# '???', '???', '???', '???', '???', '???', '???', '???',
# '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???']
# Mn = Mark, non-spacing:
# ['???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???',
# '???', '???', '???', '???', '???', '???', '???', '???', '???']
# 'DEVANAGARI SIGN INVERTED CANDRABINDU'
# 'DEVANAGARI SIGN CANDRABINDU'
# 'DEVANAGARI SIGN ANUSVARA'
# 'DEVANAGARI VOWEL SIGN OE'
# 'DEVANAGARI SIGN NUKTA'
# 'DEVANAGARI VOWEL SIGN U'
# 'DEVANAGARI VOWEL SIGN UU'
# 'DEVANAGARI VOWEL SIGN VOCALIC R'
# 'DEVANAGARI VOWEL SIGN VOCALIC RR'
# 'DEVANAGARI VOWEL SIGN CANDRA E'
# 'DEVANAGARI VOWEL SIGN SHORT E'
# 'DEVANAGARI VOWEL SIGN E'
# 'DEVANAGARI VOWEL SIGN AI'
# 'DEVANAGARI SIGN VIRAMA'
# 'DEVANAGARI STRESS SIGN UDATTA'
# 'DEVANAGARI STRESS SIGN ANUDATTA'
# 'DEVANAGARI GRAVE ACCENT'
# 'DEVANAGARI ACUTE ACCENT'
# 'DEVANAGARI VOWEL SIGN CANDRA LONG E'
# 'DEVANAGARI VOWEL SIGN UE'
# 'DEVANAGARI VOWEL SIGN UUE'
# 'DEVANAGARI VOWEL SIGN VOCALIC L'
# 'DEVANAGARI VOWEL SIGN VOCALIC LL'
# Po = punctuation, other:
# 'DEVANAGARI DANDA'
# 'DEVANAGARI DOUBLE DANDA'
# 'DEVANAGARI ABBREVIATION SIGN'
# Lm = Letter, modifier: 'DEVANAGARI SIGN HIGH SPACING DOT' = '???'
# Mc = Mark, space combining:
# 'DEVANAGARI SIGN VISARGA': '???'
# 'DEVANAGARI VOWEL SIGN OOE': '???'
# 'DEVANAGARI VOWEL SIGN AA': '???'
# 'DEVANAGARI VOWEL SIGN I': '???'
# 'DEVANAGARI VOWEL SIGN II': '???'
# 'DEVANAGARI VOWEL SIGN CANDRA O': '???'
# 'DEVANAGARI VOWEL SIGN SHORT O': ???'
# 'DEVANAGARI VOWEL SIGN O': '???'
# 'DEVANAGARI VOWEL SIGN AU': '???'
# 'DEVANAGARI VOWEL SIGN PRISHTHAMATRA E': '???'
# 'DEVANAGARI VOWEL SIGN AW': '???'


###############################################################################
# TESTING (incomplete)
###############################################################################

# TEST SPLIT_INTO_SYLLABLES

# mySyllables = list(split_into_syllables(y[6], debug=True))
# print(len(mySyllables), mySyllables)

# Incomplete!!!
specialShlokas11 = [114, 115, 116, 117, #??? ???-??????
                    120, 121,           #??? ???-??????
                    122, 123, 124, 125, #??? ???-??????
                    126, 127, 128, 129, #??? ???-??????
                    154, 155, 156, 157, #??? ???-?????????
                    160, 161, 162, 163, #??? ???-?????????
                    176, 178, 179,      #??? ???-?????????
                    262, 263, 264, 265, #??? ???-?????????
                    703, 704, 705, 706, #??? ???-??????
                    707, 708, 709,      #??? ???-?????????
                    711, 712, 713, 714, #??? ???-?????????
                    747, 748, 749, 750, #??? ???-?????????
                    793, 794, 795, 796, #??? ???-?????????
                    797, 798, 799, 800, #??? ???-?????????
                    952, 953, 954, 955, #??? ??????-?????????
                    956, 957, 958, 959 #??? ??????-?????????
                    #??? ??????-?????????
                    ]
specialShlokas12 = [118, 119, 177, 710]
specialShlokas17 = [
                    921                 #??? ??????-??????(1)
                    ]
# Test split_syllable
y = shlokasLines
for i in range(len(y)):
    if len(shlokasSyllables[i]) != 16 and '?????????????????????????????? ????????????' not in y[i] \
            and '??????????????? ????????????' not in y[i] and '?????????????????? ????????????' not in y[i] \
            and '???????????????????????????????????????' not in y[i] and '??? ????????????????????????' not in y[i] \
            and '?????????????????????????????????????????????' not in y[i] and '????????????????????????' not in y[i] \
            and i not in specialShlokas11 and i not in specialShlokas12 \
            and i not in specialShlokas17:
        print(i)
        print(y[i])
        print(len(mySyllables), mySyllables)
        break


###############################################################################
# Combine two padas of a shlok
###############################################################################

# # Combine two padas of a shlok into one line in the file
# # TODO: not perfect
# y = []
# first = True
# for line in fileLines01:
#     if '?????????????????????????????? ????????????' in line or '??????????????? ????????????' in line \
#             or '?????????????????? ????????????' in line or '???????????????????????????????????????' in line:
#         if first is False:
#             # Remove space at the end
#             y[-1] = y[-1][:-1]
#         y.append(line)
#         uvaaca = True
#     else:
#         if first:
#             # If line has a hyphen at the end, don't add space
#             if line[-1] == hyphen:
#                 y.append(line.split(hyphen)[0])
#             else:
#                 y.append(line + ' ')
#             first = False
#         else:
#             # If previous line was "_ uvaacha"
#             if uvaaca is True:
#                 # Even if this is the second paada, add it to the next line
#                 y.append(line)
#             else:
#                 y[-1] += line
#             first = True
#             uvaaca = False

# # Write clean file
# f = open('BG_clean_C01_32.txt', 'w')
# for line in y:
#     success = f.write(line+'\n')
