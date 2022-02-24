from typing import Tuple
import json
import sys

class MetaMeasure():
    """
    Measure the size of any type in bytes and report when a certain byte threshold is exceeded

    Properties:

        `tracked_bytes`: bytes counted until threshold is exceeded and it resets to 0

        `total_bytes`: total of all bytes counted by current instance of the class

        `max_size_bytes`: the threshold used to determine if `tracked_bytes` should reset

    Methods:

        `sizeof`: measure and return the size in bytes of a given object

    """

    def __init__(self, max_size_bytes=100, reset_when_threshold_exceeded=True):
        self.max_size_bytes = max_size_bytes
        self.reset_when_threshold_exceeded = reset_when_threshold_exceeded
        self.total_bytes = 0
        self.tracked_bytes = 0

    def reset(self, reset_total=False) -> None:
        """
        Reset the class' internal counters; only resets the current tracked bytes and not the total bytes counted

        Args:
            `reset_total`: reset the total bytes tracked since instatiation
        """
        self.tracked_bytes = 0
        if reset_total:
            self.total_bytes = 0
        return True

    def sizeof(self, obj, measure_flattened=False, track_bytes=True) -> Tuple[int, int, bool]:
        """
        Args:
            `obj`: the object to be measured

            `measure_flattened`: measure the bytes of the object flattened into a string

            `track_bytes`: whether the bytes measured should be added to the total bytes tracked

        Returns:
            `int`: size of object in bytes

            `int`: remaining bytes until threshold is exceeded

            `bool`: indicates if adding a similar object will exceed the threshold
        """

        size = self.measure(json.dumps(obj)) if measure_flattened else self.measure(obj)

        if track_bytes:
            self.tracked_bytes += size
            self.total_bytes += size
        
        return size, *self.evaluate()

    def measure(self, obj) -> int:
        """
        Adapted from SO:
        https://stackoverflow.com/a/58979437/12030353

        Args:
            `obj`: the object to measure

        Returns:
            `int` - size of object in bytes
        """
        size = sys.getsizeof(obj)

        if isinstance(obj, dict):
            size = size + sum(map(self.measure, obj.keys())) + sum(map(self.measure, obj.values()))
        elif isinstance(obj, (list, tuple, set, frozenset)): 
            size = size + sum(map(self.measure, obj))

        return size

    def evaluate(self) -> Tuple[int, bool]:
        """
        Returns `tuple` containing:

            `int`: remaining bytes until threshold is exceeded

            `bool`: indicates if adding a similar object will exceed the threshold
        """

        self.remaining_bytes = self.max_size_bytes - self.tracked_bytes

        if self.tracked_bytes >= self.remaining_bytes:
            if self.reset_when_threshold_exceeded:
                self.reset()
            return self.remaining_bytes, True
        else:
            return self.remaining_bytes, False

    def bytes(self, kb=0, mb=0, gb=0, tb=0) -> int:
        """
        Convert input values to bytes and return the sum

        Args:
            `kb`: kilobytes to convert to bytes

            `mb`: megabytes to convert to bytes
            
            `gb`: gigabytes to convert to bytes

            `tb`: terabytes to convert to bytes

        Return:
            `int`: sum of inputs expressed as bytes
        """
        return int(kb*1e3 + mb*1e6 + gb*1e9 + tb*1e12)