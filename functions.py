EMPTY = '@'


class Rule:

    def __init__(self, p_string=''):
        if p_string:
            self.left, right = p_string.replace(' ', '').split('->')
            self.left = self.left.strip(' []')
            self.right = list()
            new_symbol = ''
            flag = False
            for symbol in right:
                if symbol == '^' or symbol == '[':
                    flag = True
                if flag:
                    new_symbol += symbol
                    if new_symbol[0] == '^' or symbol == ']':
                        flag = False
                        new_symbol = new_symbol.strip(' []')
                        self.right.append(new_symbol)
                else:
                    self.right.append(symbol)
        else:
            self.left = ''
            self.right = list()

    def __str__(self):
        if isinstance(self.left, list):
            left = '[' + ''.join(self.left) + ']'
        else:
            left = self.left
        right = ''
        for r in self.right:
            if len(r) > 1:
                right += '[' + r + ']'
            else:
                right += r
        return left + ' -> ' + right

    def is_empty(self):
        return [EMPTY] == self.right


class Grammar:

    def __init__(self):
        self.n = set()
        self.t = set()
        self.p = list()
        self.s = 'S'

    def from_file(self, filename):

        def read_line_strip(file_object, chars=' \n'):
            return file_object.readline().strip(chars)

        self.n = list()
        self.t = list()
        self.p = list()
        self.s = ''

        f = open(filename, 'r')

        n_count = int(read_line_strip(f))
        for i in range(n_count):
            self.n.append(read_line_strip(f).strip(' []'))

        t_count = int(read_line_strip(f))
        for i in range(t_count):
            self.t.append(read_line_strip(f))

        p_count = int(read_line_strip(f))
        for i in range(p_count):
            self.p.append(Rule(read_line_strip(f)))

        self.s = read_line_strip(f).strip('[]')

        f.close()

    def to_file(self, filename):
        f = open(filename, 'w')

        f.write('Нетерминалы\n')
        for n in self.n:
            if isinstance(n, list):
                f.write('[' + ''.join(n) + ']\n')
            else:
                f.write(str(self.s) + '\n')

        f.write('\nТерминалы\n')
        for t in self.t:
            f.write(t + '\n')

        f.write('\nПравила\n')
        for p in self.p:
            f.write(str(p) + '\n')

        f.write('\nНачальный символ грамматики\n')
        if isinstance(self.s, list):
            f.write('[' + ''.join(self.s[0]) + ']')
        else:
            f.write(str(self.s))

        f.close()


if __name__ == "__main__":
    g = Grammar()
    g.from_file('INPUT.TXT')
    g.to_file('OUTPUT.TXT')
