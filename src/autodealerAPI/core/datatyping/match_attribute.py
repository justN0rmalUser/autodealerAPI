import Levenshtein
from itertools import product
from autodealerAPI.utils.tree_synonyms import Synonyms
from dataclasses import dataclass


@dataclass
class GOOD_PERC:
    ONE = 0.80
    TWO = 0.75
    THREE = 0.70
    FOUR = 0.65
    INSTANT_RETURN = 0.91


def store_attribute(name: str):
    # Подготовка текста
    name = name.lower().strip()

    # Все возможные комбинации без копии элементов
    word_list = name.split()[:4]
    one_good_ids = check_ratio(word_list, Synonyms.word_1_dict, GOOD_PERC.ONE)
    temp_elements = [one_good_ids]
    if len(word_list) >= 2:
        twos_list = [iter_to_str(element) for element in delete_copyies(list(product(word_list, repeat=2)), 2)]
        two_good_ids = check_ratio(twos_list, Synonyms.word_2_dict, GOOD_PERC.TWO)
        temp_elements.append(two_good_ids)
    if len(word_list) >= 3:
        thirds_list = [iter_to_str(element) for element in delete_copyies(list(product(word_list, repeat=3)), 3)]
        three_good_ids = check_ratio(thirds_list, Synonyms.word_3_dict, GOOD_PERC.THREE)
        temp_elements.append(three_good_ids)
    if len(word_list) >= 4:
        fourths_list = [iter_to_str(element) for element in delete_copyies(list(product(word_list, repeat=4)), 4)]
        four_good_ids = check_ratio(fourths_list, Synonyms.word_4_dict, GOOD_PERC.FOUR)
        temp_elements.append(four_good_ids)

    # Поиск соответствий
    all_elements = []
    for max_ratio, ids in sorted(temp_elements, key=lambda item: item[0], reverse=True):
        if max_ratio >= GOOD_PERC.INSTANT_RETURN:
            return ids[0]
        

    max_matches_count = 0
    max_matches = 82

    for el in all_elements:
        if all_elements.count(el) > max_matches_count:
            max_matches_count = all_elements.count(el)
            max_matches = el
        
    return max_matches

        
def delete_copyies(lst, couple_count):
    death_note = []
    for i in range(len(lst)):
        if len(set(lst[i])) < couple_count:
            death_note.append(i)
        
    for enemy in sorted(death_note, reverse=True):
        del lst[enemy]
    
    return tuple(lst)

def iter_to_str(iterator):
    res = ""
    for e in iterator:
        res+=str(e)
        res+=' '
    return res.strip()


def check_ratio(compared: list[str], pattern: dict[str, int], good_percent: float):
    max_score = 0.0
    second_score = 0.0
    match = []
    
    for variant in compared:
        # print(variant)
        for key_word in pattern:
            # print(key_word)
            ratio = Levenshtein.ratio(key_word, variant)

            if ratio >= good_percent:
                if max_score < ratio:
                    print(ratio, pattern[key_word])

                    match.insert(0, pattern[key_word])
                    max_score = ratio
                elif max_score >= ratio >= second_score:
                    print(ratio, pattern[key_word])
                    
                    match.insert(1, pattern[key_word])
                    second_score = ratio
                else:
                    match.append(pattern[key_word])
                    
    return max_score, match[:3]
