from sys import stdin


class WordSearch:

    def __init__(self, letters: list[str]):
        self.letters = letters

    @property
    def height(self):
        return len(self.letters)

    @property
    def width(self):
        return len(self.letters[0])

    def xmas_occurrences(self):
        """Return the total number of occurrences of 'XMAS'."""
        return sum(
            self._xmas_occurrences_at(i, j)
            for i in range(self.height)
            for j in range(self.width)
        )

    def _letter_at(self, i: int, j: int):
        """
        Return the letter at (i, j).

        If (i, j) are invalid coordinates, return the empty string
        ('') instead.
        """
        if not 0 <= i < self.height:
            return ""
        if not 0 <= j < self.width:
            return ""
        return self.letters[i][j]

    def _xmas_occurrences_at(self, i: int, j: int):
        """Return the number of occurrences of 'XMAS' at (i, j)."""
        if self._letter_at(i, j) != "X":
            return 0
        occurrences = 0
        if (
            self._letter_at(i, j - 1) == "M"
            and self._letter_at(i, j - 2) == "A"
            and self._letter_at(i, j - 3) == "S"
        ):
            occurrences += 1
        if (
            self._letter_at(i, j + 1) == "M"
            and self._letter_at(i, j + 2) == "A"
            and self._letter_at(i, j + 3) == "S"
        ):
            occurrences += 1

        if (
            self._letter_at(i - 1, j) == "M"
            and self._letter_at(i - 2, j) == "A"
            and self._letter_at(i - 3, j) == "S"
        ):
            occurrences += 1
        if (
            self._letter_at(i + 1, j) == "M"
            and self._letter_at(i + 2, j) == "A"
            and self._letter_at(i + 3, j) == "S"
        ):
            occurrences += 1
        if (
            self._letter_at(i - 1, j - 1) == "M"
            and self._letter_at(i - 2, j - 2) == "A"
            and self._letter_at(i - 3, j - 3) == "S"
        ):
            occurrences += 1
        if (
            self._letter_at(i - 1, j + 1) == "M"
            and self._letter_at(i - 2, j + 2) == "A"
            and self._letter_at(i - 3, j + 3) == "S"
        ):
            occurrences += 1

        if (
            self._letter_at(i + 1, j - 1) == "M"
            and self._letter_at(i + 2, j - 2) == "A"
            and self._letter_at(i + 3, j - 3) == "S"
        ):
            occurrences += 1
        if (
            self._letter_at(i + 1, j + 1) == "M"
            and self._letter_at(i + 2, j + 2) == "A"
            and self._letter_at(i + 3, j + 3) == "S"
        ):
            occurrences += 1
        return occurrences


word_search = WordSearch(stdin.read().splitlines())
print(word_search.xmas_occurrences())
