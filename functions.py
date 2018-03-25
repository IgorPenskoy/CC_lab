EMPTY = '@'


class Rule:

    def __init__(self, p_string):
        self.left, self.right = p_string.replace(' ', '').split('->')

    def __str__(self):
        return self.left + ' -> ' + self.right


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
            self.n.append(read_line_strip(f))

        t_count = int(read_line_strip(f))
        for i in range(t_count):
            self.t.append(read_line_strip(f))

        p_count = int(read_line_strip(f))
        for i in range(p_count):
            self.p.append(Rule(read_line_strip(f)))

        self.s = read_line_strip(f)

        f.close()

    def to_file(self, filename):
        f = open(filename, 'w')

        f.write('Нетерминалы\n')
        for n in self.n:
            f.write(n + '; ')

        f.write('\nТерминалы\n')
        for t in self.t:
            f.write(t + '; ')

        f.write('\nПравила\n')
        for p in self.p:
            f.write(str(p) + '; ')

        f.write('\nНачальный символ грамматики\n')
        f.write(self.s)

        f.close()


if __name__ == "__main__":
    g = Grammar()
    g.from_file('INPUT.TXT')
    g.to_file('OUTPUT.TXT')
