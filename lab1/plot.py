class SudokuPlot:
    @staticmethod
    def make_board_printer(base):
        bar = '-------------------------------\n' if base == 3 \
            else '-------------------------------------------------------------------------\n'
        lnf = '|' + ('{:2d} ' * base + '|') * base + '\n' if base == 3 \
            else '|' + (' {:2d} ' * base + ' |') * base + '\n'
        bft = bar + (lnf * base + bar) * base
        return lambda bd: print(bft.format(*(el for rw in bd for el in rw)))
