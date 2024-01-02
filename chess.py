EMPTY = 0

BOARD_MASK = 0xffffffffffffffff

# Masks for the ranks on the board.
RANKS = [RANK_1,
         RANK_2,
         RANK_3,
         RANK_4,
         RANK_5,
         RANK_6,
         RANK_7,
         RANK_8,] = [0xff << i for i in range(0, 64, 8)]

# SAN symbols for the ranks on the board.
RANK_SAN = ['1', '2', '3', '4', '5', '6', '7', '8']

# Masks for the files on the board.
FILES = [FILE_A,
         FILE_B,
         FILE_C,
         FILE_D,
         FILE_E,
         FILE_F,
         FILE_G,
         FILE_H,] = [0x0101010101010101 << i for i in range(8)]

# SAN symbols for the files on the board.
FILE_SAN = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# Masks for the squares on the board.
SQUARES = [A1, B1, C1, D1, E1, F1, G1, H1,
           A2, B2, C2, D2, E2, F2, G2, H2,
           A3, B3, C3, D3, E3, F3, G3, H3,
           A4, B4, C4, D4, E4, F4, G4, H4,
           A5, B5, C5, D5, E5, F5, G5, H5,
           A6, B6, C6, D6, E6, F6, G6, H6,
           A7, B7, C7, D7, E7, F7, G7, H7,
           A8, B8, C8, D8, E8, F8, G8, H8,] = [1 << i for i in range(64)]

# SAN symbols for the squares on the board.
SQUARE_SAN = [file + rank for rank in RANK_SAN for file in FILE_SAN]

# Numbers for the piece types.
PIECES = [PAWN,
          KNIGHT,
          BISHOP,
          ROOK,
          QUEEN,
          KING,] = [1, 2, 3, 4, 5, 6]

PIECE_SYMBOLS = ['p', 'n', 'b', 'r', 'q', 'k']

# Numbers for the color types.
COLORS = [WHITE, BLACK] = [1, 2]

class SanError(ValueError):
    '''
    A SAN parsing error.
    '''
    pass

class FenError(ValueError):
    '''
    A FEN parsing error.
    '''
    pass

class Square:
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
        return self.mask in SQUARES

    def to_rank(self):
        '''
        Gets the rank of the square.
        
        Returns:
            (int): The rank mask of the square.
        '''
        return next((rank for rank in RANKS if self.mask & rank), EMPTY)

    def to_file(self):
        '''
        Gets the file of the square.
        
        Returns:
            (int): The file mask of the square.
        '''
        return next((file for file in FILES if self.mask & file), EMPTY)

    def to_san(self):
        '''
        Gets the SAN of the square.

        Returns:
            (str): The SAN of the square.
        '''
        if not self.is_legal():
            return ''

        # Get the SAN of the square.
        san_index = SQUARES.index(self.mask)

        return SQUARE_SAN[san_index]

    @classmethod
    def from_san(cls, san):
        '''
        Creates a square from SAN.

        Params:
            san (str): SAN for a square.

        Returns:
            (chess.Square): The new square.
        '''
        if not san in SQUARE_SAN:
            raise SanError(f'Invalid square \'{san}\'')

        # Get the square mask.
        mask_index = SQUARE_SAN.index(san)

        return Square(SQUARES[mask_index])

class Piece:
    def __init__(self, piece, color):
        '''
        Creates a piece.

        Params:
            piece (int): A piece type.
            color (int): A piece color.

        Returns:
            (chess.Piece): The new piece.
        '''
        self.piece = piece
        self.color = color

    def __repr__(self):
        '''
        Gets a representation of the piece with the symbol.

        Returns:
            (str): The representation.
        '''
        return f'<Piece symbol=\'{self.to_symbol()}\'>'

    def to_symbol(self):
        '''
        Gets the symbol for the piece.

        Returns:
            (str): The symbol.
        '''
        if not self.piece in PIECES or not self.color in COLORS:
            return ''

        # Get the piece symbol.
        symbol_index = PIECES.index(self.piece)
        symbol = PIECE_SYMBOLS[symbol_index]

        # White pieces are upper-case.
        if self.color == WHITE:
            symbol = symbol.upper()

        return symbol

    @classmethod
    def from_symbol(cls, symbol):
        '''
        Creates a piece from a symbol.

        Params:
            symbol (str): A symbol.

        Returns:
            (chess.Piece): The new peice.
        '''
        lower_symbol = symbol.lower()
        
        if not lower_symbol in PIECE_SYMBOLS:
            raise FenError(f'Invalid symbol \'{symbol}\'')

        # Get the piece type and color.
        piece_index = PIECE_SYMBOLS.index(lower_symbol)
        piece = PIECES[piece_index]
        color = WHITE if symbol.isupper() else BLACK

        return Piece(piece, color)
