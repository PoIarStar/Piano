import sys
from winsound import Beep as play
from instruction import instruction
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from piano import Ui_MainWindow
import sqlite3


con = sqlite3.connect('melodies.sqlite')
cur = con.cursor()


class MainWindow(QMainWindow, Ui_MainWindow):

    # Класс основного окна

    def __init__(self):
        self.octaves = ['субконтроктава', 'контроктава', 'большая', 'малая', 'первая', 'вторая', 'третья', 'четвёртая',
                        'пятая']
        self.octave_num = 4
        super().__init__()
        self.setupUi(self)

        # Запись, воспроизводящаяся в данный момент
        self.is_rec = False
        self.music = ''
        self.music_name = ''

        # Список всех нот
        self.notes = [[self.play_contr_re, self.play_contr_mi_b, self.play_contr_mi, self.play_contr_fa,
                       self.play_contr_sol_b, self.play_contr_sol, self.play_contr_la_b, self.play_contr_la,
                       self.play_contr_si_b, self.play_contr_si],
                      [self.play_big_do, self.play_big_re_b, self.play_big_re, self.play_big_mi_b,
                       self.play_big_mi, self.play_big_fa, self.play_big_sol_b, self.play_big_sol,
                       self.play_big_la_b, self.play_big_la, self.play_big_si_b, self.play_big_si],
                      [self.play_small_do, self.play_small_re_b, self.play_small_re, self.play_small_mi_b,
                       self.play_small_mi, self.play_small_fa, self.play_small_sol_b, self.play_small_sol,
                       self.play_small_la_b, self.play_small_la, self.play_small_si_b, self.play_small_si],
                      [self.play_oc_1_do, self.play_oc_1_re_b, self.play_oc_1_re, self.play_oc_1_mi_b,
                       self.play_oc_1_mi, self.play_oc_1_fa, self.play_oc_1_sol_b, self.play_oc_1_sol,
                       self.play_oc_1_la_b, self.play_oc_1_la, self.play_oc_1_si_b, self.play_oc_1_si],
                      [self.play_oc_2_do, self.play_oc_2_re_b, self.play_oc_2_re, self.play_oc_2_mi_b,
                       self.play_oc_2_mi, self.play_oc_2_fa, self.play_oc_2_sol_b, self.play_oc_2_sol,
                       self.play_oc_2_la_b, self.play_oc_2_la, self.play_oc_2_si_b, self.play_oc_2_si],
                      [self.play_oc_3_do, self.play_oc_3_re_b, self.play_oc_3_re, self.play_oc_3_mi_b,
                       self.play_oc_3_mi, self.play_oc_3_fa, self.play_oc_3_sol_b, self.play_oc_3_sol,
                       self.play_oc_3_la_b, self.play_oc_3_la, self.play_oc_3_si_b, self.play_oc_3_si],
                      [self.play_oc_4_do, self.play_oc_4_re_b, self.play_oc_4_re, self.play_oc_4_mi_b,
                       self.play_oc_4_mi, self.play_oc_4_fa, self.play_oc_4_sol_b, self.play_oc_4_sol,
                       self.play_oc_4_la_b, self.play_oc_4_la, self.play_oc_4_si_b, self.play_oc_4_si],
                      [self.play_oc_5_do]]

        # Кнопки нот
        self.contr_re.clicked.connect(self.play_contr_re)
        self.contr_mi_b.clicked.connect(self.play_contr_mi_b)
        self.contr_mi.clicked.connect(self.play_contr_mi)
        self.contr_fa.clicked.connect(self.play_contr_fa)
        self.contr_sol_b.clicked.connect(self.play_contr_sol_b)
        self.contr_sol.clicked.connect(self.play_contr_sol)
        self.contr_la_b.clicked.connect(self.play_contr_la_b)
        self.contr_la.clicked.connect(self.play_contr_la)
        self.contr_si_b.clicked.connect(self.play_contr_si_b)
        self.contr_si.clicked.connect(self.play_contr_si)
        self.big_do.clicked.connect(self.play_big_do)
        self.big_re_b.clicked.connect(self.play_big_re_b)
        self.big_re.clicked.connect(self.play_big_re)
        self.big_mi_b.clicked.connect(self.play_big_mi_b)
        self.big_mi.clicked.connect(self.play_big_mi)
        self.big_fa.clicked.connect(self.play_big_fa)
        self.big_sol_b.clicked.connect(self.play_big_sol_b)
        self.big_sol.clicked.connect(self.play_big_sol)
        self.big_la_b.clicked.connect(self.play_big_la_b)
        self.big_la.clicked.connect(self.play_big_la)
        self.big_si_b.clicked.connect(self.play_big_si_b)
        self.big_si.clicked.connect(self.play_big_si)
        self.small_do.clicked.connect(self.play_small_do)
        self.small_re_b.clicked.connect(self.play_small_re_b)
        self.small_re.clicked.connect(self.play_small_re)
        self.small_mi_b.clicked.connect(self.play_small_mi_b)
        self.small_mi.clicked.connect(self.play_small_mi)
        self.small_fa.clicked.connect(self.play_small_fa)
        self.small_sol_b.clicked.connect(self.play_small_sol_b)
        self.small_sol.clicked.connect(self.play_small_sol)
        self.small_la_b.clicked.connect(self.play_small_la_b)
        self.small_la.clicked.connect(self.play_small_la)
        self.small_si_b.clicked.connect(self.play_small_si_b)
        self.small_si.clicked.connect(self.play_small_si)
        self.oc_1_do.clicked.connect(self.play_oc_1_do)
        self.oc_1_re_b.clicked.connect(self.play_oc_1_re_b)
        self.oc_1_re.clicked.connect(self.play_oc_1_re)
        self.oc_1_mi_b.clicked.connect(self.play_oc_1_mi_b)
        self.oc_1_mi.clicked.connect(self.play_oc_1_mi)
        self.oc_1_fa.clicked.connect(self.play_oc_1_fa)
        self.oc_1_sol_b.clicked.connect(self.play_oc_1_sol_b)
        self.oc_1_sol.clicked.connect(self.play_oc_1_sol)
        self.oc_1_la_b.clicked.connect(self.play_oc_1_la_b)
        self.oc_1_la.clicked.connect(self.play_oc_1_la)
        self.oc_1_si_b.clicked.connect(self.play_oc_1_si_b)
        self.oc_1_si.clicked.connect(self.play_oc_1_si)
        self.oc_2_do.clicked.connect(self.play_oc_2_do)
        self.oc_2_re_b.clicked.connect(self.play_oc_2_re_b)
        self.oc_2_re.clicked.connect(self.play_oc_2_re)
        self.oc_2_mi_b.clicked.connect(self.play_oc_2_mi_b)
        self.oc_2_mi.clicked.connect(self.play_oc_2_mi)
        self.oc_2_fa.clicked.connect(self.play_oc_2_fa)
        self.oc_2_sol_b.clicked.connect(self.play_oc_2_sol_b)
        self.oc_2_sol.clicked.connect(self.play_oc_2_sol)
        self.oc_2_la_b.clicked.connect(self.play_oc_2_la_b)
        self.oc_2_la.clicked.connect(self.play_oc_2_la)
        self.oc_2_si_b.clicked.connect(self.play_oc_2_si_b)
        self.oc_2_si.clicked.connect(self.play_oc_2_si)
        self.oc_3_do.clicked.connect(self.play_oc_3_do)
        self.oc_3_re_b.clicked.connect(self.play_oc_3_re_b)
        self.oc_3_re.clicked.connect(self.play_oc_3_re)
        self.oc_3_mi_b.clicked.connect(self.play_oc_3_mi_b)
        self.oc_3_mi.clicked.connect(self.play_oc_3_mi)
        self.oc_3_fa.clicked.connect(self.play_oc_3_fa)
        self.oc_3_sol_b.clicked.connect(self.play_oc_3_sol_b)
        self.oc_3_sol.clicked.connect(self.play_oc_3_sol)
        self.oc_3_la_b.clicked.connect(self.play_oc_3_la_b)
        self.oc_3_la.clicked.connect(self.play_oc_3_la)
        self.oc_3_si_b.clicked.connect(self.play_oc_3_si_b)
        self.oc_3_si.clicked.connect(self.play_oc_3_si)
        self.oc_4_do.clicked.connect(self.play_oc_4_do)
        self.oc_4_re_b.clicked.connect(self.play_oc_4_re_b)
        self.oc_4_re.clicked.connect(self.play_oc_4_re)
        self.oc_4_mi_b.clicked.connect(self.play_oc_4_mi_b)
        self.oc_4_mi.clicked.connect(self.play_oc_4_mi)
        self.oc_4_fa.clicked.connect(self.play_oc_4_fa)
        self.oc_4_sol_b.clicked.connect(self.play_oc_4_sol_b)
        self.oc_4_sol.clicked.connect(self.play_oc_4_sol)
        self.oc_4_la_b.clicked.connect(self.play_oc_4_la_b)
        self.oc_4_la.clicked.connect(self.play_oc_4_la)
        self.oc_4_si_b.clicked.connect(self.play_oc_4_si_b)
        self.oc_4_si.clicked.connect(self.play_oc_4_si)
        self.oc_5_do.clicked.connect(self.play_oc_5_do)

        # Проигрывание и запись
        self.file_button.clicked.connect(self.file_select)
        self.play_button.clicked.connect(self.play)
        self.stop_button.clicked.connect(self.stop)
        self.rec_button.clicked.connect(self.rec)
        self.save_button.clicked.connect(self.save)

        # Вывод инструкции
        self.help_button.clicked.connect(self.help)

    # Функции нот
    def play_contr_re(self):
        play(37, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'37-{int(self.duration.value() * 10)} '

    def play_contr_mi_b(self):
        play(39, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'39-{int(self.duration.value() * 10)} '

    def play_contr_mi(self):
        play(41, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'41-{int(self.duration.value() * 10)} '

    def play_contr_fa(self):
        play(44, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'44-{int(self.duration.value() * 10)} '

    def play_contr_sol_b(self):
        play(46, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'46-{int(self.duration.value() * 10)} '

    def play_contr_sol(self):
        play(49, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'49-{int(self.duration.value() * 10)} '

    def play_contr_la_b(self):
        play(52, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'52-{int(self.duration.value() * 10)} '

    def play_contr_la(self):
        play(55, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'55-{int(self.duration.value() * 10)} '

    def play_contr_si_b(self):
        play(58, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'58-{int(self.duration.value() * 10)} '

    def play_contr_si(self):
        play(62, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'62-{int(self.duration.value() * 10)} '

    def play_big_do(self):
        play(65, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'65-{int(self.duration.value() * 10)} '

    def play_big_re_b(self):
        play(69, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'69-{int(self.duration.value() * 10)} '

    def play_big_re(self):
        play(73, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'73-{int(self.duration.value() * 10)} '

    def play_big_mi_b(self):
        play(78, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'78-{int(self.duration.value() * 10)} '

    def play_big_mi(self):
        play(82, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'82-{int(self.duration.value() * 10)} '

    def play_big_fa(self):
        play(87, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'87-{int(self.duration.value() * 10)} '

    def play_big_sol_b(self):
        play(93, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'93-{int(self.duration.value() * 10)} '

    def play_big_sol(self):
        play(98, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'98-{int(self.duration.value() * 10)} '

    def play_big_la_b(self):
        play(104, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'104-{int(self.duration.value() * 10)} '

    def play_big_la(self):
        play(110, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'110-{int(self.duration.value() * 10)} '

    def play_big_si_b(self):
        play(117, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'117-{int(self.duration.value() * 10)} '

    def play_big_si(self):
        play(123, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'123-{int(self.duration.value() * 10)} '

    def play_small_do(self):
        play(131, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'131-{int(self.duration.value() * 10)} '

    def play_small_re_b(self):
        play(139, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'139-{int(self.duration.value() * 10)} '

    def play_small_re(self):
        play(147, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'147-{int(self.duration.value() * 10)} '

    def play_small_mi_b(self):
        play(156, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'156-{int(self.duration.value() * 10)} '

    def play_small_mi(self):
        play(165, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'165-{int(self.duration.value() * 10)} '

    def play_small_fa(self):
        play(175, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'175-{int(self.duration.value() * 10)} '

    def play_small_sol_b(self):
        play(185, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'185-{int(self.duration.value() * 10)} '

    def play_small_sol(self):
        play(196, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'196-{int(self.duration.value() * 10)} '

    def play_small_la_b(self):
        play(208, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'208-{int(self.duration.value() * 10)} '

    def play_small_la(self):
        play(220, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'220-{int(self.duration.value() * 10)} '

    def play_small_si_b(self):
        play(233, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'233-{int(self.duration.value() * 10)} '

    def play_small_si(self):
        play(245, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'245-{int(self.duration.value() * 10)} '

    def play_oc_1_do(self):
        play(262, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'262-{int(self.duration.value() * 10)} '

    def play_oc_1_re_b(self):
        play(277, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'277-{int(self.duration.value() * 10)} '

    def play_oc_1_re(self):
        play(294, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'294-{int(self.duration.value() * 10)} '

    def play_oc_1_mi_b(self):
        play(311, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'311-{int(self.duration.value() * 10)} '

    def play_oc_1_mi(self):
        play(330, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'330-{int(self.duration.value() * 10)} '

    def play_oc_1_fa(self):
        play(349, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'349-{int(self.duration.value() * 10)} '

    def play_oc_1_sol_b(self):
        play(370, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'370-{int(self.duration.value() * 10)} '

    def play_oc_1_sol(self):
        play(392, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'392-{int(self.duration.value() * 10)} '

    def play_oc_1_la_b(self):
        play(415, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'415-{int(self.duration.value() * 10)} '

    def play_oc_1_la(self):
        play(440, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'440-{int(self.duration.value() * 10)} '

    def play_oc_1_si_b(self):
        play(466, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'466-{int(self.duration.value() * 10)} '

    def play_oc_1_si(self):
        play(494, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'494-{int(self.duration.value() * 10)} '

    def play_oc_2_do(self):
        play(523, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'523-{int(self.duration.value() * 10)} '

    def play_oc_2_re_b(self):
        play(554, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'554-{int(self.duration.value() * 10)} '

    def play_oc_2_re(self):
        play(587, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'587-{int(self.duration.value() * 10)} '

    def play_oc_2_mi_b(self):
        play(622, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'622-{int(self.duration.value() * 10)} '

    def play_oc_2_mi(self):
        play(659, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'659-{int(self.duration.value() * 10)} '

    def play_oc_2_fa(self):
        play(698, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'698-{int(self.duration.value() * 10)} '

    def play_oc_2_sol_b(self):
        play(740, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'740-{int(self.duration.value() * 10)} '

    def play_oc_2_sol(self):
        play(784, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'784-{int(self.duration.value() * 10)} '

    def play_oc_2_la_b(self):
        play(831, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'831-{int(self.duration.value() * 10)} '

    def play_oc_2_la(self):
        play(880, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'880-{int(self.duration.value() * 10)} '

    def play_oc_2_si_b(self):
        play(932, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'932-{int(self.duration.value() * 10)} '

    def play_oc_2_si(self):
        play(988, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'988-{int(self.duration.value() * 10)} '

    def play_oc_3_do(self):
        play(1046, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1046-{int(self.duration.value() * 10)} '

    def play_oc_3_re_b(self):
        play(1109, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1109-{int(self.duration.value() * 10)} '

    def play_oc_3_re(self):
        play(1174, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1174-{int(self.duration.value() * 10)} '

    def play_oc_3_mi_b(self):
        play(1244, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1244-{int(self.duration.value() * 10)} '

    def play_oc_3_mi(self):
        play(1318, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1318-{int(self.duration.value() * 10)} '

    def play_oc_3_fa(self):
        play(1397, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1397-{int(self.duration.value() * 10)} '

    def play_oc_3_sol_b(self):
        play(1480, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1480-{int(self.duration.value() * 10)} '

    def play_oc_3_sol(self):
        play(1568, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1568-{int(self.duration.value() * 10)} '

    def play_oc_3_la_b(self):
        play(1661, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1661-{int(self.duration.value() * 10)} '

    def play_oc_3_la(self):
        play(1760, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1760-{int(self.duration.value() * 10)} '

    def play_oc_3_si_b(self):
        play(1865, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1865-{int(self.duration.value() * 10)} '

    def play_oc_3_si(self):
        play(1976, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'1976-{int(self.duration.value() * 10)} '

    def play_oc_4_do(self):
        play(2093, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'2093-{int(self.duration.value() * 10)} '

    def play_oc_4_re_b(self):
        play(2217, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'2217-{int(self.duration.value() * 10)} '

    def play_oc_4_re(self):
        play(2349, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'2349-{int(self.duration.value() * 10)} '

    def play_oc_4_mi_b(self):
        play(2489, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'2489-{int(self.duration.value() * 10)} '

    def play_oc_4_mi(self):
        play(2637, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'2637-{int(self.duration.value() * 10)} '

    def play_oc_4_fa(self):
        play(2794, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'2794-{int(self.duration.value() * 10)} '

    def play_oc_4_sol_b(self):
        play(2960, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'2960-{int(self.duration.value() * 10)} '

    def play_oc_4_sol(self):
        play(3136, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'3136-{int(self.duration.value() * 10)} '

    def play_oc_4_la_b(self):
        play(3322, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'3322-{int(self.duration.value() * 10)} '

    def play_oc_4_la(self):
        play(3520, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'3520-{int(self.duration.value() * 10)} '

    def play_oc_4_si_b(self):
        play(3729, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'3729-{int(self.duration.value() * 10)} '

    def play_oc_4_si(self):
        play(3951, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'3951-{int(self.duration.value() * 10)} '

    def play_oc_5_do(self):
        play(4186, int(self.duration.value() * 1000))
        if self.is_rec:
            self.music += f'4186-{int(self.duration.value() * 10)} '

    # Игра с клвиатуры
    def keyPressEvent(self, event):
        note = None
        if event.key() == Qt.Key_Up or event.key() == Qt.Key_W:
            self.duration.setValue(self.duration.value() + 0.1)
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_S:
            self.duration.setValue(self.duration.value() - 0.1)
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
            self.octave_num = (self.octave_num + 8) % 9
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
            self.octave_num = (self.octave_num + 10) % 9
        elif event.key() == Qt.Key_1:
            self.octave_num = 0
        elif event.key() == Qt.Key_2:
            self.octave_num = 1
        elif event.key() == Qt.Key_3:
            self.octave_num = 2
        elif event.key() == Qt.Key_4:
            self.octave_num = 3
        elif event.key() == Qt.Key_5:
            self.octave_num = 4
        elif event.key() == Qt.Key_6:
            self.octave_num = 5
        elif event.key() == Qt.Key_7:
            self.octave_num = 6
        elif event.key() == Qt.Key_8:
            self.octave_num = 7
        elif event.key() == Qt.Key_9:
            self.octave_num = 8
        elif event.key() == Qt.Key_F:
            if self.octave_num < 2:
                return
            else:
                note = 0
        elif event.key() == Qt.Key_T:
            if self.octave_num < 2 or self.octave_num == 8:
                return
            else:
                note = 1
        elif event.key() == Qt.Key_G:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 2
        elif event.key() == Qt.Key_Y:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 3
        elif event.key() == Qt.Key_H:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 4
        elif event.key() == Qt.Key_J:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 5
        elif event.key() == Qt.Key_I:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 6
        elif event.key() == Qt.Key_K:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 7
        elif event.key() == Qt.Key_O:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 8
        elif event.key() == Qt.Key_L:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 9
        elif event.key() == Qt.Key_P:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 10
        elif event.key() == Qt.Key_Semicolon:
            if self.octave_num < 1 or self.octave_num == 8:
                return
            else:
                note = 11
        if note is not None:
            self.notes[self.octave_num - 1][note]()
        self.octave.setText(f'Текущая октава: {self.octaves[self.octave_num]}')

    # Функции записи и проигрывания
    def rec(self):
        self.music = ''
        self.is_rec = True
        self.textBrowser.setText('')

    def stop(self):
        self.is_rec = False

    def play(self):
        for i in self.music.split():
            sound = i.split('-')
            play(int(sound[0]), int(sound[1]) * 100)

    def save(self):
        name, ok_pressed = QInputDialog.getText(self, 'Сохранение', 'Придумайте название своей композиции')
        if name:
            cur.execute(f"INSERT INTO melodies(name, notes) VALUES ('{name}', '{self.music}')")
            con.commit()

    def file_select(self):
        cur.execute('SELECT name FROM melodies')
        musics = [i[0] for i in cur.fetchall()]
        music, ok_pressed = QInputDialog.getItem(self, 'Выбор мелодии', 'Выберите запись из списка:', musics, 0, False)
        cur.execute(f"SELECT * FROM melodies WHERE name = '{music}'")
        self.music_name, self.music = cur.fetchone()
        self.textBrowser.setText(music)

    # Вывод документации
    def help(self):
        docs = QMessageBox(self)
        docs.setWindowTitle('Инструкция пользователя')
        docs.setText(instruction)
        docs.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
