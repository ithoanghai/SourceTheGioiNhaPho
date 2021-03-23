from functools import lru_cache

text_list = ('không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín', 'mười')


class NumToVnStr:
    def __init__(self, hang_chuc='mươi', nghin='nghìn', tu='tư', nam='lăm', linh='linh', ty='tỷ', is_empty=True):
        self.hang_chuc = hang_chuc
        self.tram = 'trăm'
        self.nghin = nghin
        self.trieu = 'triệu'
        self.ty = ty
        self.mot = 'mốt'
        self.tu = tu
        self.nam = nam
        self.linh = linh
        self.is_empty = is_empty

    @lru_cache()
    def to_vn_str(self, s):
        return self._arbitrary(s.lstrip('0'))

    def _int(self, c):
        return ord(c) - ord('0') if c else 0

    def _LT1e2(self, s):
        if len(s) <= 1:
            return text_list[self._int(s)]
        if s[0] == '1':
            ret = text_list[10]
        else:
            ret = text_list[self._int(s[0])]
            if self.hang_chuc:
                ret += ' ' + self.hang_chuc
            elif s[1] == '0':
                ret += ' mươi'
        if s[1] != '0':
            ret += ' '
            if s[1] == '1' and s[0] != '1':
                ret += self.mot
            elif s[1] == '4' and s[0] != '1':
                ret += self.tu
            elif s[1] == '5':
                ret += self.nam
            else:
                ret += text_list[self._int(s[1])]
        return ret

    def _LT1e3(self, s):
        if len(s) <= 2:
            return self._LT1e2(s)
        if s == '000':
            return ''
        ret = text_list[self._int(s[0])] + ' ' + self.tram
        if s[1] != '0':
            ret += ' ' + self._LT1e2(s[1:])
        elif s[2] != '0':
            ret += ' ' + self.linh + ' ' + text_list[self._int(s[2])]
        return ret

    def _LT1e9(self, s):
        if len(s) <= 3: return self._LT1e3(s)
        if s == '000000' or s == '000000000':
            return ''
        mid = len(s) % 3 if len(s) % 3 else 3
        left, right = self._LT1e3(s[:mid]), self._LT1e9(s[mid:])
        hang = self.nghin if len(s) <= 6 else self.trieu
        if not left:
            if not self.is_empty:
                return right
            else:
                return text_list[0] + ' ' + hang + ' ' + right
        if not right:
            return left + ' ' + hang
        return left + ' ' + hang + ' ' + right

    def _arbitrary(self, s):
        if len(s) <= 9: return self._LT1e9(s)
        mid = len(s) % 9 if len(s) % 9 else 9
        left, right = self._LT1e9(s[:mid]), self._arbitrary(s[mid:])
        hang = ' '.join([self.ty] * ((len(s) - mid) // 9))
        if not left:
            if not self.is_empty:
                return right
            elif right:
                return text_list[0] + ' ' + hang + ', ' + right
            else:
                return right
        if not right:
            return left + ' ' + hang
        return left + ' ' + hang + ', ' + right
