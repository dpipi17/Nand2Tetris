

class VMWriter:

    def __init__(self, output_file_path):
        self.output_file = open(output_file_path, 'w')

    def write_push(self, segment, index):
        self.output_file.write('  push {} {}\n'.format(segment, str(index)))

    def write_pop(self, segment, index):
        self.output_file.write('  pop {} {}\n'.format(segment, str(index)))

    def write_arithmetic(self, command):
        self.output_file.write('  {}\n'.format(command))

    def write_label(self, label):
        self.output_file.write('label {}\n'.format(label))

    def write_go_to(self, label):
        self.output_file.write('  goto {}\n'.format(label))

    def write_if(self, label):
        self.output_file.write('  if-goto {}\n'.format(label))

    def write_call(self, name, n_args):
        self.output_file.write('  call {} {}\n'.format(name, str(n_args)))

    def write_function(self, name, n_locals):
        self.output_file.write('function {} {}\n'.format(name, str(n_locals)))

    def write_return(self):
        self.output_file.write('  return\n')

    def close(self):
        self.output_file.close()



