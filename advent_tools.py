import os
import sys
import torch


__all__ = ["PuzzleSetup", "Timer"]


class PuzzleSetup:
    """
    Class for setting up advent of code puzzles.
    """

    def __init__(self, file):
        """
        :arg file: the puzzle Python file.
        """
        self.verbose = False
        self.gpu = False
        self._set_input_file(file)
        self._set_kwargs()

        # Set CUDA device
        self.device = torch.device("cpu")
        if self.gpu:
            assert torch.cuda.is_available(), "CUDA is not available."
            device = torch.device("cuda:0")
            if self.verbose:
                print(f"Using CUDA device {torch.cuda.get_device_name(0)}\n")

    def _set_input_file(self, file):
        """
        Parse user input to determine the puzzle setup.

        :arg file: the puzzle Python file.
        """
        argv = sys.argv
        self.input_file = "input.txt"
        if len(argv) > 1 and not argv[1].startswith("--"):
            self.input_file = f"{argv[1]}.txt"
            abspath = os.path.join(os.path.dirname(file), self.input_file)
            if not os.path.exists(abspath):
                raise IOError(
                    f"Invalid input '{' '.join(argv[1:])}'."
                    f"File '{argv[1]}' does not exist."
                )

    def _set_kwargs(self):
        """
        Set any keyword arguments
        """
        argv = sys.argv
        s = 1 if argv[1].startswith("--") else 2
        if len(argv) > s:
            for kwarg in argv[s:]:
                assert kwarg.startswith("--"), f"Invalid kwarg '{kwarg}'."
                if hasattr(self, kwarg[2:]):
                    self.__setattr__(kwarg[2:], True)
                else:
                    raise IOError(f"Unrecognised kwarg '{kwarg}'.")
