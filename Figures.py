from typing import Callable

class Figures:
    def __init__(self, name: str, player):
        self.name = name
        self.player = player

    def __str__(self):
        return self.name.upper() if self.player else self.name

class Pawn(Figures):
    def __init__(self, player: bool):
        super().__init__('p', player)
        self.first_move = True
        self.under_passant = False
    
    def get_attack_list(self, position: complex, position_info: Callable):
        signature = 1 if self.player else -1
        attack_list = set()

        for move in {complex(1, 1), complex(-1, 1)}:
            new_position = position + signature * move
            
            if position_info(new_position) != None and position_info(new_position).player != self.player:
                attack_list.add((position, new_position))
            
            elif position_info(new_position) == None and position_info(new_position - signature * complex(0, 1)) != None:
                possible_passant = new_position - signature * complex(0, 1)
                if position_info(possible_passant).name == 'p' and position_info(possible_passant).player != self.player and position_info(possible_passant).under_passant:
                    attack_list.add((position, new_position, possible_passant))
        
        new_position = position + signature * complex(0, 1)


        if position_info(new_position) == None:
            attack_list.add((position, new_position))
        
        if self.first_move:
            new_position = new_position + signature * complex(0, 1)
            if position_info(new_position) == None and position_info(new_position - signature * complex(0, 1)) == None:
                attack_list.add((position, new_position))

        return attack_list

class Rook(Figures):
    def __init__(self, player: bool):
        super().__init__('r', player)
        self.can_cast = True

    def get_attack_list(self, position: complex, position_info: Callable):
        attack_list = set()

        for move in {complex(0, 1), complex(0, -1), complex(1, 0), complex(-1, 0)}:
            new_position = position
            while True:
                new_position += move

                if not (1 <= new_position.real <= 8 and 1 <= new_position.imag <= 8):
                    break
                
                elif position_info(new_position) != None and position_info(new_position).player == self.player:
                    break

                else:
                    attack_list.add((position, new_position))
                
                if position_info(new_position) != None and position_info(new_position).player != self.player:
                    break
        
        return attack_list
                
class Queen(Figures):
    def __init__(self, player: bool):
        super().__init__('q', player)

    def get_attack_list(self, position: complex, position_info: Callable):
        attack_list = set()

        for move in {complex(0, 1), complex(0, -1), complex(1, 0), complex(-1, 0), complex(1, 1), complex(1, -1), complex(-1, 1), complex(-1, -1)}:
            new_position = position
            while True:
                new_position += move

                if not (1 <= new_position.real <= 8 and 1 <= new_position.imag <= 8):
                    break
                
                elif position_info(new_position) != None and position_info(new_position).player == self.player:
                    break

                else:
                    attack_list.add((position, new_position))
                
                if position_info(new_position) != None and position_info(new_position).player != self.player:
                    break
        
        return attack_list    

class Bishop(Figures):
    def __init__(self, player: bool):
        super().__init__('b', player)

    def get_attack_list(self, position: complex, position_info: Callable):
        attack_list = set()

        for move in {complex(1, 1), complex(1, -1), complex(-1, 1), complex(-1, -1)}:
            new_position = position
            while True:
                new_position += move

                if not (1 <= new_position.real <= 8 and 1 <= new_position.imag <= 8):
                    break
                
                elif position_info(new_position) != None and position_info(new_position).player == self.player:
                    break

                else:
                    attack_list.add((position, new_position))
                
                if position_info(new_position) != None and position_info(new_position).player != self.player:
                    break
        
        return attack_list

class Knight(Figures):
    def __init__(self, player: bool):
        super().__init__('n', player)
        self.can_cast = True

    def get_attack_list(self, position: complex, position_info: Callable):
        attack_list = set()

        for move in {complex(2, 1), complex(-2, 1), complex(2, -1), complex(-2, -1), complex(1, 2), complex(-1, 2), complex(1, -2), complex(-1, -2)}:
            new_position = position + move
            if not (1 <= new_position.real <= 8 and 1 <= new_position.imag <= 8):
                continue
                
            elif position_info(new_position) != None and position_info(new_position).player == self.player:
                continue

            else:
                attack_list.add((position, new_position))
        
        return attack_list

class King(Figures):
    def __init__(self, player: bool):
        super().__init__('k', player)
        self.can_cast = True

    def get_attack_list(self, position: complex, position_info: Callable):
        attack_list = set()

        for move in {complex(0, 1), complex(0, -1), complex(1, 0), complex(-1, 0), complex(1, 1), complex(1, -1), complex(-1, 1), complex(-1, -1)}:
            new_position = position + move

            if not (1 <= new_position.real <= 8 and 1 <= new_position.imag <= 8):
                continue
                
            elif position_info(new_position) != None and position_info(new_position).player == self.player:
                continue

            else:
                attack_list.add((position, new_position))
        
        return attack_list
    
    def get_castling_list(self, position: complex, position_info: Callable, safe_position:Callable):
        castling_list = set()

        if self.can_cast:
            self.can_cast = False
            long_cast = complex(1, position.imag)
            short_cast = complex(8, position.imag)

            if position_info(long_cast) != None and position_info(long_cast).name == 'r' and position_info(long_cast).can_cast and safe_position(complex(2, position.imag)):

                new_position, flag = position - complex(1, 0), True

                while new_position != long_cast:
                    if position_info(new_position) != None:
                        flag = False
                        break
                    else:
                        new_position = new_position - complex(1, 0)
                
                if flag:
                    castling_list.add((position, new_position + complex(1, 0), 'long'))
                
            if position_info(short_cast) != None and position_info(short_cast).name == 'r' and position_info(short_cast).can_cast and safe_position(complex(7, position.imag)):

                new_position, flag = position + complex(1, 0), True

                while new_position != short_cast:
                    if position_info(new_position) != None:
                        flag = False
                        break
                    else:
                        new_position = new_position + complex(1, 0)
                
                if flag:
                    castling_list.add((position, new_position - complex(1, 0), 'short'))

        return castling_list