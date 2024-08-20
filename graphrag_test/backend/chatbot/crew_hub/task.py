class Task:
    def __init__(self, name, input, input_format, output_format, description):
        self.name = name
        self.input = input
        self.input_format = input_format
        self.output_format = output_format
        self.description = description