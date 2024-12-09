class Block:
    """Describe a contiguous sequence of spaces."""

    def __init__(self, block_id: int | None, start: int, size: int):
        self.block_id = block_id
        self.start = start
        self.size = size

    def __repr__(self):
        return f"[{self.block_id} ({self.start}, {self.size})]"

    def connected(self, other: "Block"):
        return self.start + self.size == other.start

    def checksum(self):
        if self.block_id is None:
            return 0
        # Sum of consecutive integers formula adapted from ChatGPT
        return (
            self.block_id
            * (self.start + self.start + self.size - 1)
            * (self.size)
            // 2
        )


class Disk:

    def __init__(self, data: str):
        self.blocks: list[Block] = []
        next_start = 0
        for i, block_size in enumerate(map(int, data)):
            if i % 2 == 0:
                block_id = i // 2
            else:
                block_id = None
            self.blocks.append(Block(block_id, next_start, block_size))
            next_start += block_size

    def __repr__(self):
        blocks = sorted(self.blocks, key=lambda block: block.start)
        output = []
        for block in blocks:
            if block.block_id is None:
                symbol = "."
            else:
                symbol = str(block.block_id)
            output.append(symbol * block.size)
        return "".join(output)

    def move_blocks(self):
        blocks = [block for block in self.blocks if block.block_id is not None]
        for block in reversed(blocks):
            for gap in self.blocks:
                if gap == block:
                    break
                if gap.block_id is not None:
                    continue
                if gap.size < block.size:
                    continue
                new_gap = Block(None, block.start, block.size)
                block.start = gap.start
                gap.start += block.size
                gap.size -= block.size
                self.add_gap(new_gap)
                # Sorting is not smart but whatever, it ran fast enough
                self.blocks.sort(key=lambda block: block.start)
                break

    def add_gap(self, gap: Block):
        for block in reversed(self.blocks):
            if gap.connected(block) and block.block_id is None:
                self.blocks.remove(block)
                gap.size += block.size
                break
        for block in self.blocks:
            if block.connected(gap) and block.block_id is None:
                block.size += gap.size
                break
        else:
            self.blocks.append(gap)

    def checksum(self):
        return sum(block.checksum() for block in self.blocks)


disk = Disk(input())
disk.move_blocks()
print(disk.checksum())
