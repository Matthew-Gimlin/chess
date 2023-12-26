EMPTY = 0

BOARD_MASK = 0xffffffffffffffff

# Masks for the squares on the board.
SQUARES = [A1, B1, C1, D1, E1, F1, G1, H1,
           A2, B2, C2, D2, E2, F2, G2, H2,
           A3, B3, C3, D3, E3, F3, G3, H3,
           A4, B4, C4, D4, E4, F4, G4, H4,
           A5, B5, C5, D5, E5, F5, G5, H5,
           A6, B6, C6, D6, E6, F6, G6, H6,
           A7, B7, C7, D7, E7, F7, G7, H7,
           A8, B8, C8, D8, E8, F8, G8, H8,] = [1 << i for i in range(64)]

# Masks for the ranks on the board.
RANKS = [RANK_1,
         RANK_2,
         RANK_3,
         RANK_4,
         RANK_5,
         RANK_6,
         RANK_7,
         RANK_8,] = [0xff << i for i in range(0, 64, 8)]

# Masks for the files on the board.
FILES = [FILE_A,
         FILE_B,
         FILE_C,
         FILE_D,
         FILE_E,
         FILE_F,
         FILE_G,
         FILE_H,] = [0x0101010101010101 << i for i in range(8)]

class SanError(ValueError):
    '''
    A SAN parsing error.
    '''
    pass

class Square:
    '''
    A square on the board.
    
    Members:
        mask (int): A mask for a square on the board.
    '''
    def __init__(self, mask=EMPTY):
        '''
        Creates a square.

        Params:
            mask (int): A mask for the square on the board.
        
        Returns:
            (chess.Square): The new square.
        '''
        self.mask = mask

    def __repr__(self):
        '''
        Gets a representation of the square with the mask and SAN.

        Returns:
            (str): The representation.
        '''
        return f'<Square mask=0x{self.mask:x} san=\'{self.to_san()}\'>'

    def is_legal(self):
        '''
        Checks if the square is on the board.
        
        Returns:
            (bool): If the square is on the board.
        '''
        return self.mask & BOARD_MASK

    def to_rank(self):
        '''
        Gets the rank of the square.
        
        Returns:
            (int): The rank mask of the square.
        '''
        rank = RANK_1
        while rank & BOARD_MASK:
            if self.mask & rank:
                return rank
            rank <<= 8

        return EMPTY

    def to_file(self):
        '''
        Gets the file of the square.
        
        Returns:
            (int): The file mask of the square.
        '''
        file = FILE_A
        while file & BOARD_MASK:
            if self.mask & file:
                return file
            file <<= 1

        return EMPTY

    def to_san(self):
        '''
        Gets the SAN of the square.

        Returns:
            (str): The SAN of the square.
        '''
        if not self.on_board():
            return ''
        
        san = ''
        
        # Get the file.
        file = FILE_A
        for file_char in 'abcdefgh':
            if self.mask & file:
                san += file_char
                break
            file <<= 1

        # Get the rank.
        rank = RANK_1
        for rank_char in '12345678':
            if self.mask & rank:
                san += rank_char
                break
            rank <<= 8

        return san

    @classmethod
    def from_san(cls, san):
        '''
        Creates a square from SAN.

        Params:
            san (str): A square in SAN.

        Returns:
            (chess.Square): The new square.
        '''
        if len(san) != 2:
            raise SanError(f'Invalid length {len(san)} (expects 2)')

        # Parse the rank and file.
        san = san.lower()
        san_file = san[0]
        san_rank = san[1]

        mask = A1

        # Get the file.
        for file_char in 'abcdefgh':
            if file_char == san_file:
                break
            mask <<= 1
        else:
            raise SanError(f'Invalid file \'{san_rank}\'')

        # Get the rank.
        for rank_char in '12345678':
            if rank_char == san_rank:
                break
            mask <<= 8
        else:
            raise SanError(f'Invalid rank \'{san_rank}\'')

        return cls(mask)
