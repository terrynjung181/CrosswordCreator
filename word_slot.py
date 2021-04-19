class WordSlot:
  """
  A WordSlot object represents a consecutive horizontal or vertical white
  space in a crossword layout.
  
  Attributes:
  [start] - a tuple representing the index position of the first character
          for the empty slot.
  [direction] - a string that represents orientation of WordSlot. Could either
              be ACROSS or DOWN
  [length] - an integer representing the length of the empty slot.
  [Overlap] - a list of ids (integers) of other WordSlot objects that overlap
            with this WordSlot object on the crossword layout. Initialized as
            an empty list.
  [Word] - a string that represents the legitimate word that belongs in the  
          empty slot. Initialized as empty string.
  [Definition] - a string that is the legitimate corresponding definition of the
              word. Intialized as empty string.
  """

  def __init__(self, start, direction, length):
    self.start = start
    self.direction = direction
    self.length = length
    self.overlap = []
    self.word = ""
    self.definition = ""

  def __repr__(self):
    """
    Object representation when printed out.
    """
    return "Start: " + str(self.start) + ", Dir: " + self.direction + ", Length: " + str(self.length) +", Overlap: " + str(self.overlap) + "\n"
  
  def get_start(self, ind = 3):
    """
    Input:  [ind] - Integer representing index of desired coordinate self.start.
                  Default to 3 which returns the entire tuple
    """
    if ind == 0:
      return self.start[0]
    elif ind == 1:
      return self.start[1]
    else:
      return self.start

  def get_direction(self):
    return self.direction

  def get_length(self):
    return self.length

  def add_overlap(self, id_num):
    """
    Input:  [id_num] - Integer representing id_number of a WordSlot object that
                    should be appended to overlap list.
    """
    self.overlap.append(id_num)

  def get_overlap(self):
      return self.overlap

  def set_word(self, word):
    """
    Input:  [word] - String that represents legitimate word that belongs in the
                    following slot.
    """
    self.word = word
  
  def get_word(self):
    return self.word
  
  def set_definition(self, definition):
    """
    Input:  [definition] - String that represents legitimate definition that 
                        belongs in the following slot.
    """
    self.definition = definition
  
  def get_definition(self):
    return self.definition
