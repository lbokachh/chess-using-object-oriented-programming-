from Logic import Chessboard

class Interface:
    def __init__(self):
        self.cb = Chessboard() 
        self.chessboard_background = {complex(v, g):'\033[37m' for v in range(1, 9) for g in range(1, 9)}

    def start_motion(self):
        for k in self.chessboard_background.keys():
            self.chessboard_background[k] = '\033[37m'

        for elem in self.cb.friends_under_attack():
            self.chessboard_background[elem] = '\033[31m'

        return None

    def finish_motion(self, position):
        for k in self.chessboard_background.keys():
            self.chessboard_background[k] = '\033[37m'

        for elem in self.cb.final_move_list(position):
            self.chessboard_background[elem[1]] = '\033[32m'

        return None
    
    def draw_board(self):
        non_symbol = '.'
        
        if self.cb.player:
            print('\033[37m/ A B C D E F G H \\')
            for i in range(8, 0, -1):
                line = f'\033[37m{str(i)} '
                for j in range(1, 9):
                    line += f'{self.chessboard_background[complex(j, i)]}{self.cb.chessboard[complex(j, i)] if self.cb.chessboard[complex(j, i)] != None else non_symbol}' + ' '
                line += f'\033[37m{str(i)}'
                print(line)
            print('\033[37m\\ A B C D E F G H /')
              
        else:
            print('/ A B C D E F G H \\')
            for i in range(1, 9):
                line = f'{str(i)} '
                for j in range(1, 9):
                    line += f'{self.chessboard_background[complex(j, i)]}{self.cb.chessboard[complex(j, i)] if self.cb.chessboard[complex(j, i)] != None else non_symbol}' + ' '
                line += f'{str(i)}'
                print(line)
            print('\\ A B C D E F G H /')
        
        return None
    
    @staticmethod
    def chose_mode():
        print('Выберите режим игры: ')
        print('1. Новая игра')
        print('2. Загрузить с аннотации')
        chosen_variant = input('Введите выбранный вариант >> ')
        return chosen_variant
    
    @staticmethod
    def chose_enemy():
        print('Выберите, против кого будете играть: ')
        print('1. Человек')
        print('2. Компьютер')
        chosen_variant = input('Введите выбранный вариант >> ')
        return chosen_variant
    
if __name__ == '__main__':
    intf = Interface()
    intf.start_motion()
    intf.finish_motion(complex(2, 2))
    intf.draw_board()