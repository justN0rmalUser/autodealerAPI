import Levenshtein
from itertools import product
from .tree_synonyms import Synonyms
from dataclasses import dataclass


@dataclass
class GOOD_PERC:
    ONE = 0.80
    TWO = 0.75
    THREE = 0.70
    FOUR = 0.65
    INSTANT_RETURN = 0.91


def store_attribute(name: str) -> int:
    # Подготовка текста
    if not name:
        return 82
    
    name = name.lower().strip()
    word_list = name.split()[:4]
        
    
    # Все возможные комбинации без копии элементов
    temp_elements = _check_ratio(word_list, Synonyms.word_1_dict, GOOD_PERC.ONE)
        
    if len(word_list) >= 2:
        twos_list = [_iter_to_str(element) for element in _delete_copyies(list(product(word_list, repeat=2)), 2)]
        temp_elements.extend(
            _check_ratio(
                twos_list, 
                Synonyms.word_2_dict, 
                GOOD_PERC.TWO
            )
        )
    
    if len(word_list) >= 3:
        thirds_list = [_iter_to_str(element) for element in _delete_copyies(list(product(word_list, repeat=3)), 3)]
        temp_elements.extend(
            _check_ratio(
                thirds_list, 
                Synonyms.word_3_dict, 
                GOOD_PERC.THREE
            )
        )
    
    if len(word_list) == 4:
        fourths_list = [_iter_to_str(element) for element in _delete_copyies(list(product(word_list, repeat=4)), 4)]
        temp_elements.extend(
            _check_ratio(
                fourths_list, 
                Synonyms.word_4_dict, 
                GOOD_PERC.FOUR
            )
        )

    # Поиск соответствий
    all_elements = []
    for ratio, tree_id in sorted(temp_elements, key=lambda item: item[0], reverse=True):
        if ratio >= GOOD_PERC.INSTANT_RETURN:
            return tree_id
        all_elements.append(tree_id)
        
    max_tree_id_count: int = 0
    most_likely_tree_id: int = 82

    for el in set(all_elements):
        if all_elements.count(el) > max_tree_id_count:
            max_tree_id_count = all_elements.count(el)
            most_likely_tree_id = el
        
    return most_likely_tree_id

        
def _delete_copyies(lst, couple_count):
    death_note = []
    for i in range(len(lst)):
        if len(set(lst[i])) < couple_count:
            death_note.append(i)
        
    for enemy in sorted(death_note, reverse=True):
        del lst[enemy]
    
    return tuple(lst)

def _iter_to_str(iterator):
    res = ""
    for e in iterator:
        res+=str(e)
        res+=' '
    return res.strip()


def _check_ratio(compared: list[str], pattern: dict[str, int], good_percent: float) -> list[tuple[float, int]]:
    match = []
    
    for variant in compared:
        # print(variant)
        for key_word in pattern:
            # print(key_word)
            ratio = Levenshtein.ratio(key_word, variant)

            if ratio >= good_percent:
                match.append(
                    (ratio, pattern[key_word])
                )
                    
    return match
