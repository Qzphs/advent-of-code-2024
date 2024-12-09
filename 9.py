import collections


class Disk:

    def __init__(self, data: str):
        self.blocks = collections.deque()
        for i, block_size in enumerate(map(int, data)):
            if i % 2 == 0:
                self.blocks.extend([i // 2] * block_size)
            else:
                self.blocks.extend([None] * block_size)

    def checksum(self):
        blocks = self.blocks.copy()
        checksum = 0
        i = 0
        while blocks:
            block = blocks.popleft()
            while block is None:
                if not blocks:
                    return checksum
                block = blocks.pop()
            checksum += i * block
            i += 1
        return checksum


print(Disk(input()).checksum())
