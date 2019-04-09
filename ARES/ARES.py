import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


_COLS = ('wavelength', 'nlines', 'depth', 'fwhm',
        'EW', 'EWerr', 'amplitude', 'sigma', 'mean')


class ARES:
    def __init__(self, *arg, **kwargs):
        self._config_created = False
        self.kwargs = kwargs
        self._create_config()
        self.outputfile = self.kwargs.get('fileout', 'test.ares')

    @classmethod
    def from_config(cls, fname):
        with open(fname) as lines:
            kwargs = dict()
            for line in lines:
                line = line.split('=')
                line = list(map(lambda s: s.replace(' ', ''), line))
                kwargs[line[0]] = kwargs[1]
        return cls(**kwargs)

    def _create_config(self):
        fout =  f"specfits='{self.kwargs.get('specfits')}'\n"
        fout += f"readlinedat='{self.kwargs.get('readlinedat', 'cdo.dat')}'\n"
        fout += f"fileout='{self.kwargs.get('fileout', 'aresout.dat')}'\n"
        fout += f"lambdai={self.kwargs.get('lambdai', 3000)}\n"
        fout += f"lambdaf={self.kwargs.get('lambdaf', 8000)}\n"
        fout += f"smoothder={self.kwargs.get('smoothder', 6)}\n"
        fout += f"space={self.kwargs.get('space', 3.0)}\n"
        fout += f"rejt={self.kwargs.get('rejt', '3;5764,5766,6047,6052,6068,6076')}\n"
        fout += f"lineresol={self.kwargs.get('lineresol', 0.05)}\n"
        fout += f"miniline={self.kwargs.get('miniline', 2)}\n"
        fout += f"plots_flag={self.kwargs.get('plots_flag', 0)}\n"
        fout += f"rvmask='{self.kwargs.get('rvmask', '3,6021.8,6024.06,6027.06,6024.06,20')}'\n"
        with open('mine.opt', 'w') as f:
            f.writelines(fout)
        self._config_created = True

    def run(self, verbose=False):
        if not self._config_created:
            self._create_config()
        if verbose:
            print('Running ARES...')
        os.system('ARES > /dev/null')
        if verbose:
            print(f'Done! Result saved in {self.kwargs.get("fileout", "aresout.dat")}')

    @staticmethod
    def read_output(fname):
        return ARESOutput(fname)

    @staticmethod
    def get_rv(fname='logARES.txt'):
        with open(fname, 'r') as lines:
            for line in lines:
                if line.startswith('Velocidade radial'):
                    break
        rv = line.rpartition(':')[-1]
        return float(rv)


class ARESOutput:
    def __init__(self, fname, *args, **kwargs):
        self.fname = fname
        self.df = pd.read_csv(self.fname, sep=r'\s+', header=None)
        self.df.columns = _COLS
        df.set_index('wavelength', inplace=True)

    def percent_diff(self, other, col):
        """Find the percent difference between two ARES output for a given column.
        Is given by:
            (self.df.col - other.df.col) / self.df.col * 100

        Input
        -----
        other : ARESOutput object
            The result from another spectrum
        col : str
            The col for which to calculate the difference

        Output
        ------
        p : np.ndarray
            An array with the percetange differences between the two outputs for a given column
        """
        if not isinstance(other, ARESOutput):
            raise TypeError(f'other is of type {type(other)} which is not compatible for this method')
        if not col in _COLS:
            raise ValueError(f'The following columns are allowed: {_COLS}')
        p = (self.df[col] - other.df[col]) / self.df[col] * 100
        return p.values

    def plot(self, col1, col2=None, *args, **kwargs):
        if col2 is None:
            col2 = col1
            col1 = 'wavelength'
        if not (col1 in _COLS) or not (col2 in _COLS):
            raise ValueError(f'The following columns are allowed: {_COLS}')

        plt.plot(self.df[col1], self.df[col2], 'o', *args, **kwargs)
        plt.xlabel(col1)
        plt.ylabel(col2)

    def mse(self, other, col):
        """Measure the mean square error between two results for a given column.
        Is given by:
            1/N * sum((x1-x2)^2)

        Input
        -----
        other : ARESOutput object
            The result from another spectrum
        col : str
            The col for which to calculate the difference

        Output
        ------
        r : float
            The MSE
        """
        if not isinstance(other, ARESOutput):
            raise TypeError(f'other is of type {type(other)} which is not compatible for this method')
        if not col in _COLS:
            raise ValueError(f'The following columns are allowed: {_COLS}')
        N = max((len(self.df), len(other.df)))
        df = self.df.join(other.df, how='outer', lsuffix='_l', rsuffix='_r')
        return 1/N * (np.sum((df[col+'_l'] - df[col+'_r'])**2))