from molecule import Molecule

class QMEngine(object):
    def __init__(self, input_file=None):
        if input_file != None:
            self.load_input(input_file)

    def load_input(self, input_file):
        raise NotImplementedError


class EnginePsi4(QMEngine):

    def load_input(self, input_file):
        """ Load a Psi4 input file.
        Exmaple:
        memory 12 gb

        molecule {
        0 1
        H 0 0 1
        H 0 0 2
        units angstrom
        no_reorient
        symmetry c1
        }

        set globals {{
            basis         6-31+g*
            freeze_core   True
            guess         sad
            scf_type      df
            print         1
        }}

        set_num_threads(1)
        gradient('mp2')
        """
        found_gradient = False
        self.template = ""
        self.molecule = Molecule()
        with open(input_file) as infile:
            for line in infile:
                line = line.strip



class EngineQChem(QMEngine):
    def load_input(self, input_file):
        raise NotImplementedError("QChem engine has not been implemented yet!")
