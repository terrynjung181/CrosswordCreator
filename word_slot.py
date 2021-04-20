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
  [Overlap] - a list of (id, row, col) triplets -- id is the id of the WordSlot object that overlaps,
              and (row, col) is the location of this overlap in the crossword
              with this WordSlot object on the crossword layout. Initialized as
            an empty list.
  [Words] - a list of python dictionaries, each of which represent a legitimate word that can belong 
            in the empty slot. Initialized as None.
  [Definition] - a string that is the legitimate corresponding definition of the
              word. Intialized as empty string.
  """

  def __init__(self, start, direction, length):
    self.start = start
    self.direction = direction
    self.length = length
    self.overlap = []
    self.words = None
    self.definition = ""

  def __repr__(self):
    """
    Object representation when printed out.
    """
    return "Start: " + str(self.start) + ", Dir: " + self.direction + \
      ", Length: " + str(self.length) + ", Overlap: " + str(self.overlap) + \
      ", Words: " + (str([i['word'] for i in self.words]) if self.words is not None else "None") + "\n"
  
  
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

  def set_words(self, words):
    """
    Input:  [words] - String that represents legitimate word that belongs in the
                    following slot.
    """
    self.words = words
  
  def get_words(self):
    return self.words
  
  def set_definition(self, definition):
    """
    Input:  [definition] - String that represents legitimate definition that 
                        belongs in the following slot.
    """
    self.definition = definition
  
  def get_definition(self):
    return self.definition
