from typing import Tuple, List

import numpy as np
import warnings


class FileParser:
    """
    FilParser: Parses .npy files from googles QuickDraws data set
    https://github.com/googlecreativelab/quickdraw-dataset
    """

    def __init__(self) -> None:

        self.files = [
            'apple.npy',
            'computer.npy',
            'tree.npy',
            'pencil.npy'
        ]

    @staticmethod
    def _shuffle(x: np.ndarray, y: np.ndarray, seed: int = 99) -> Tuple[np.ndarray, np.ndarray]:
        np.random.seed(seed)
        """
        Randomizes two nd.arrays with the same length in unison
        :param x: images
        :param y: hot one encoding of y
        :param seed:
        :return: Randomized x, y
        """
        if len(x) != len(y):
            raise ValueError('x, y cannot have different lengths!')

        # Allocate space
        shuffled_x = np.empty(x.shape, dtype=x.dtype)
        shuffled_y = np.empty(y.shape, dtype=x.dtype)
        # All indexes in random order
        permutation = np.random.permutation(len(x))
        # Shuffle
        for old_index, new_index in enumerate(permutation):
            shuffled_x[new_index] = x[old_index]
            shuffled_y[new_index] = y[old_index]

        return shuffled_x, shuffled_y

    def clear(self) -> None:
        """
        Clears all files in self.files
        :return: None
        """
        self.files.clear()

    def update(self, files: List[str]) -> None:
        """
        Update the files that self.load() is going to load drawings from
        :param files: List of new files to add
        :return:
        """
        # Loop through new files
        for file in files:
            # Check that is a .npy file
            extension = file.split(".")[-1]
            if extension != ".npy":
                warnings.warn(f"{file} excluded! file extension is .{extension} instead of .npy!")
                continue
            # Check that does not already exist
            if file not in self.files:
                self.files.append(file)

    def load(self, train_amount: int = 300, test_amount: int = 50, seed: int = 99) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Returns training and test data sets
        :param train_amount: Total amount of training data to parse
        :param test_amount: Total amount of test data to parse
        :param seed: for randomizing array
        :return: Tuple[train_x, train_y, test_x, test_y]
        """
        # Cannot load less than one drawing per file
        if 0 < test_amount < len(self.files) or 0 < train_amount < len(self.files):

            raise ValueError("Amount is smaller than files in Class, Cannot load less than one file per file")

        # Cannot load from zero files
        if not len(self.files):
            raise ValueError(f"self.files is currently Empty, Wont load anything!")

        # Prepare variables for loading
        amount_of_files = len(self.files)
        train_amount_per_file = train_amount // amount_of_files
        test_amount_per_file = test_amount // amount_of_files
        offset = train_amount_per_file

        train_x = np.empty((train_amount_per_file * amount_of_files, 1, 28, 28), dtype='float32')
        train_y = np.empty((train_amount_per_file * amount_of_files, amount_of_files, 1), dtype='int')

        test_x = np.empty((test_amount_per_file * amount_of_files, 1, 28, 28), dtype='float32')
        test_y = np.empty((test_amount_per_file * amount_of_files, amount_of_files, 1), dtype='int')

        # Loop through all files
        for i, file in enumerate(self.files):

            # Load images from .npy file
            images = np.load(f"data/{file}").astype('float32') / 255.

            # Reshape that each image will be in a 1X28X28 format
            images = images.reshape(-1, 1, 28, 28)

            # hot one encoding of labels
            y = np.zeros((amount_of_files, 1))
            y[i] = 1

            # Indices for storing data
            train_start = i * train_amount_per_file
            train_end = train_start + train_amount_per_file
            test_start = i * test_amount_per_file
            test_end = test_start + test_amount_per_file

            train_x[train_start:train_end] = images[train_start:train_end]
            train_y[train_start:train_end] = y

            test_x[test_start:test_end] = images[test_start + offset:test_end + offset]
            test_y[test_start:test_end] = y

        # Shuffle the data
        train_x, train_y = self._shuffle(train_x, train_y, seed)
        test_x, test_x = self._shuffle(test_x, test_x, seed)

        return train_x, train_y, test_x, test_y

















