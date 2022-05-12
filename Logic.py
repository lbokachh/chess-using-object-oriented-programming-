from Figures import Pawn, Rook, Queen, Knight, King, Bishop

class Chessboard:
    def __init__(self):
        self.chessboard = {complex(v, g):None for v in range(1, 9) for g in range(1, 9)}
        
        for i in range(1, 9):
            self.chessboard[complex(i, 2)] = Pawn(True)
            self.chessboard[complex(i, 7)] = Pawn(False)
        
        self.chessboard[1 + 1j] = Rook(True)
        self.chessboard[2 + 1j] = Knight(True)
        self.chessboard[3 + 1j] = Bishop(True)
        self.chessboard[4 + 1j] = Queen(True)
        self.chessboard[5 + 1j] = King(True)
        self.chessboard[6 + 1j] = Bishop(True)
        self.chessboard[7 + 1j] = Knight(True)
        self.chessboard[8 + 1j] = Rook(True)

        self.chessboard[1 + 8j] = Rook(False)
        self.chessboard[2 + 8j] = Knight(False)
        self.chessboard[3 + 8j] = Bishop(False)
        self.chessboard[4 + 8j] = Queen(False)
        self.chessboard[5 + 8j] = King(False)
        self.chessboard[6 + 8j] = Bishop(False)
        self.chessboard[7 + 8j] = Knight(False)
        self.chessboard[8 + 8j] = Rook(False)
        
        self.player = True

    def position_info(self, position: complex):
        return self.chessboard.get(position)

    def is_position_safe(self, position: complex):
        enemies_list = {k for k in self.chessboard.keys() if self.chessboard[k] != None and self.chessboard[k].player != self.player}

        flag = True

        for k in enemies_list:
            enemy_trajectory = set(map(lambda x: x[1], self.chessboard[k].get_attack_list(k, self.position_info)))

            if position in enemy_trajectory:
                flag = False
                break
        
        return flag
    
    def king_position(self):
        for k in self.chessboard.keys():
            if self.chessboard[k] != None and self.chessboard[k].name == 'k' and self.chessboard[k].player == self.player:
                return k
    
    def check_mate(self):
        kp = self.king_position()
        flag = True
        solutions = set()

        if not self.is_position_safe(kp):
            friends_list = {k for k in self.chessboard.keys() if self.chessboard[k] != None and self.chessboard[k].player == self.player}
            
            for friend in friends_list:
                for move in self.chessboard[friend].get_attack_list(friend, self.position_info):
                    v = self.chessboard[move[1]]
                    self.chessboard[move[1]] = self.chessboard[move[0]]
                    self.chessboard[move[0]] = None
                    kp = self.king_position()

                    if self.is_position_safe(kp):
                        solutions.add(move)
                    
                    self.chessboard[move[0]] = self.chessboard[move[1]]
                    self.chessboard[move[1]] = v

            if len(solutions) > 0:
                flag = False
        else:
            flag = False

        return flag, solutions
    
    def update_pawn(self, position: complex, figure: str):
        match figure:
            case 'Слон':
                self.chessboard[position] = Bishop(self.player)
            case 'Ладья':
                self.chessboard[position] = Rook(self.player)
                self.chessboard.can_cast = False
            case 'Конь':
                self.chessboard[position] = Knight(self.player)
            case 'Ферзь':
                self.chessboard[position] = Queen(self.player)
            case _:
                return False, 'Нет такой фигуры'

        return True, None

    def final_move_list(self, position: complex):
        final_move_list = set()
        
        if self.chessboard[position] != None and self.chessboard[position].player == self.player:
            final_move_list = final_move_list.union(self.chessboard[position].get_attack_list(position, self.position_info))

            if not self.is_position_safe(self.king_position()):
                final_move_list = final_move_list.intersection(self.check_mate()[1])
            
            elif self.chessboard[position].name == 'k' and self.chessboard[position].player == self.player:
                final_move_list = final_move_list.union(self.chessboard[position].get_castling_list(position, self.position_info, self.is_position_safe))
                
        return final_move_list
    
    def friends_under_attack(self):
        friendly_units = {k for k in self.chessboard.keys() if self.chessboard[k] != None and self.chessboard[k].player == self.player}
        friends_under_attack = set()

        for friend in friendly_units:
            if not self.is_position_safe(friend):
                friends_under_attack.add(friend)
        
        return friends_under_attack