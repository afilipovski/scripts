import datetime

class TinyLogger:
    def __init__(self, name : str, period : datetime.timedelta):
        buffer = []

        try:
            file = open(f"{name}.log","r")
            lines = file.readlines()
            for line in lines:
                parts = line.partition("] ")
                time = parts[0][1:]
                timestamp = datetime.datetime.fromisoformat(time)
                if timestamp > datetime.datetime.now() - period:
                    buffer.append(line)
        except FileNotFoundError:
            pass
        file = open(f"{name}.log","w")
        for line in buffer:
            file.write(line)
        self.file = file

    def __del__(self):
        self.file.close()

    def log(self, message):
        self.file.write(f"[{str(datetime.datetime.now())}] {message}\n")