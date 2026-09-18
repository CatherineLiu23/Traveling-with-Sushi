import json

class RhymeChecker:
    def __init__(self, rhymes_file='prompts/rhymes.json'):
        with open(rhymes_file, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        self.char_to_rhyme = {}
        for key, val in raw.items():
            if isinstance(val, dict) and 'chars' in val:
                chars_str = val['chars']
                rhyme_name = val.get('name', key)
            elif isinstance(val, str):
                chars_str = val
                rhyme_name = key
            else:
                continue
            for ch in chars_str:
                self.char_to_rhyme[ch] = rhyme_name
        print(f"韵书加载完成，共 {len(self.char_to_rhyme)} 字")

    def get_rhyme(self, char):
        return self.char_to_rhyme.get(char)

    def check_rhyme(self, chars):
        if not chars:
            return True, ""
        first = self.get_rhyme(chars[0])
        if not first:
            return False, f"「{chars[0]}」不在韵书中"
        for ch in chars[1:]:
            cur = self.get_rhyme(ch)
            if not cur:
                return False, f"「{ch}」不在韵书中"
            if cur != first:
                return False, f"「{ch}」( {cur} ) 与「{chars[0]}」( {first} ) 不同韵"
        return True, "押韵成功"