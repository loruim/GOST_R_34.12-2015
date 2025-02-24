class key:
    def __init__(self, path : str):
        with open(path, "r") as f:
            content = f.read()
            if len(content) != 256:
                raise Warning(f"len key != 256 bits")
        new_content = ""
        for _ in range(64):
            new_content += str(hex(int(content[:4], 2))[2:])
            content = content[4:]
        self.key = new_content
        self.__Separation()
        
    def __Separation(self):
        round_keys = []
        block_size = 8

        for _ in range(3):
            for i in range(8):
                start = i * block_size
                end = start + block_size
                round_keys.append(self.key[start:end])

        for i in range(7, -1, -1):
            round_keys.append(round_keys[i])

        self.round_key = round_keys