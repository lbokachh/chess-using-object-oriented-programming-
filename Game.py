from Interface import Interface
from copy import deepcopy

class Game:
    def __init__(self):
        self.interface = Interface()
        self.save_board = []
    
    def rollback(self):
        if len(self.save_board) > 1:
            self.save_board.pop()
            self.interface.cb.chessboard = self.save_board[-1][0]
            self.interface.cb.player = self.save_board.pop()[1]
        else:
            print('Откат хода невозможен!')
        return None
    
    def start_game(self):
        game_mode = self.interface.chose_mode()
        if game_mode == '1':
            self.new_game()
        elif game_mode == '2':
            print('Данный режим ещё в разработке')
        else:
            print('Нет выбранного режима!')
        return None

    def new_game(self):
        chosen_enemy = self.interface.chose_enemy()
        if chosen_enemy == '1':
            self.play_game()
        elif chosen_enemy == '2':
            print('Данный вариант игры ещё в разработке')
        else:
            print('Нет выбранного варианта!')
        return None
    
    @staticmethod
    def coordinate_2_complex(coordinate: str):
        vertical_coordinate_dict = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
        return complex(vertical_coordinate_dict.get(coordinate[0]), int(coordinate[1])) 

    def play_game(self):
        self.interface.start_motion()
        self.save_board.append((deepcopy(self.interface.cb.chessboard), self.interface.cb.player))
        self.interface.draw_board()
        while not self.interface.cb.check_mate()[0]:
            line = input('Выберите фигуру или действие >> ')
            
            if line == 'Откат хода':
                self.rollback()
                self.interface.start_motion()
                self.save_board.append((deepcopy(self.interface.cb.chessboard), self.interface.cb.player))
                self.interface.draw_board()

            
            elif len(line) == 2:
                position = self.coordinate_2_complex(line)

                if self.interface.cb.chessboard.get(position) != None and self.interface.cb.chessboard.get(position).player == self.interface.cb.player:
                    self.interface.finish_motion(position)
                    self.interface.draw_board()

                    possible_trajectory = list(self.interface.cb.final_move_list(position))
                    possible_final_points = list(map(lambda x: x[1], possible_trajectory))

                    while True:
                        line = input('Введите конечную координату или действие >> ')

                        if line == 'Выбрать другую фигуру':
                            self.interface.cb.chessboard = self.save_board[-1][0]
                            self.interface.cb.player = self.save_board[-1][1]
                            break

                        elif len(line) == 2:
                            new_position = self.coordinate_2_complex(line)

                            if new_position in possible_final_points:
                                chosen_trajectory = possible_trajectory[possible_final_points.index(new_position)]

                                if len(chosen_trajectory) == 2:
                                    self.interface.cb.chessboard[chosen_trajectory[1]] = self.interface.cb.chessboard[chosen_trajectory[0]]
                                    self.interface.cb.chessboard[chosen_trajectory[0]] = None
                                else:
                                    if chosen_trajectory[2] == 'long':
                                        self.interface.cb.chessboard[chosen_trajectory[1]] = self.interface.cb.chessboard[chosen_trajectory[0]]
                                        self.interface.cb.chessboard[chosen_trajectory[0]] = None
                                        self.interface.cb.chessboard[complex(3, chosen_trajectory[1].imag)] = self.interface.cb.chessboard[complex(1, chosen_trajectory[1].imag)]
                                        self.interface.cb.chessboard[complex(1, chosen_trajectory[1].imag)] = None
                                    
                                    elif chosen_trajectory[2] == 'short':
                                        self.interface.cb.chessboard[chosen_trajectory[1]] = self.interface.cb.chessboard[chosen_trajectory[0]]
                                        self.interface.cb.chessboard[chosen_trajectory[0]] = None
                                        self.interface.cb.chessboard[complex(6, chosen_trajectory[1].imag)] = self.interface.cb.chessboard[complex(8, chosen_trajectory[1].imag)]
                                        self.interface.cb.chessboard[complex(8, chosen_trajectory[1].imag)] = None
                                    
                                    else:
                                        self.interface.cb.chessboard[chosen_trajectory[1]] = self.interface.cb.chessboard[chosen_trajectory[0]]
                                        self.interface.cb.chessboard[chosen_trajectory[0]] = None
                                        self.interface.cb.chessboard[chosen_trajectory[2]] = None
                                
                                if (self.interface.cb.chessboard[chosen_trajectory[1]].name == 'k' or self.interface.cb.chessboard[chosen_trajectory[1]].name == 'r') and self.interface.cb.chessboard[chosen_trajectory[1]].can_cast:
                                    self.interface.cb.chessboard[chosen_trajectory[1]].can_cast = False
            
                                if self.interface.cb.chessboard[chosen_trajectory[1]].name == 'p':
                                    if abs(new_position - position) == 2.0:
                                        self.interface.cb.chessboard[chosen_trajectory[1]].under_passant = True
                                    
                                    if self.interface.cb.chessboard[chosen_trajectory[1]].first_move:
                                        self.interface.cb.chessboard[chosen_trajectory[1]].first_move = False

                                    if chosen_trajectory[1].imag == 8 or chosen_trajectory[1].imag == 1:
                                        self.interface.cb.update_pawn(chosen_trajectory[1], input('Введите фигуру для замены >> '))


                                for k in self.interface.cb.chessboard.keys():
                                    if self.interface.cb.chessboard[k] != None and self.interface.cb.chessboard[k].name == 'p' and self.interface.cb.chessboard[k].player != self.interface.cb.player:
                                        self.interface.cb.chessboard[k].under_passant = False
                                
                                self.interface.cb.player = not self.interface.cb.player
                                self.interface.start_motion()
                                self.save_board.append((deepcopy(self.interface.cb.chessboard), self.interface.cb.player))
                                self.interface.draw_board()
                                break
                            else:
                                print('Данный ход невозможен')
                        
                        else:
                            print('Команда не распознана')
                else:
                    print('Команда не распознана')

            else:
                print('Команда не распознана')
        
        self.interface.start_motion()   
        self.interface.draw_board()
        print('Игра закончена!')
        print(f'Выиграл {1 if not self.interface.cb.player else 2} игрок')
    
        return None

if __name__ == '__main__':
    chessgame = Game()
    chessgame.start_game()