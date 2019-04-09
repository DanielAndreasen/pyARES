# pyARES
A package to run [ARES](https://github.com/sousasag/ARES), configure the input file, and read the output.

This require `ARES` to already be installed in your `PATH`.

# Requirements
This was developed on python=3.6 and use `f-strings`, and is thus not compatible with versions lower than that.
It also requires `matplotlib`, `numpy`, and `pandas`.

If you would like to run this on an earlier version, it is straight forward to fix it, however you should consider
[using python3](https://python3statement.org/) instead as it is only a [matter of time](https://pythonclock.org/)
before python2.7 is no longer supported.


# Usage
## Run `ARES` with some standard inputs

```python
from ARES import ARES
config = {'specfits': 'path/to/fits',
          'readlinedat': 'path/to/linelist',
          'fileout': 'path/to/output'}
a = ARES(**config)  # Setup ARES
a.run()             # Run ARES
output = ARES.read_output(config['fileout']) # Return an ARESOutput object
rv = ARES.get_rv()  # Get the RV as meausered by ARES
```

## Plotting with ARESOutput
```python
# Run ARES and get the output object
output = ARES.read_output(config['fileout'])
plt.figure()
output.plot('EW')  # Plot EW against wavelength

plt.figure()
output.plot('EW', 'EWerr') # EWerr against EW
# plot method also takes standard matplotlib inputs
plt.show()
```

## Comparing two outputs
```python
o1 = ARES.read_output('path/to/output1')
o2 = ARES.read_output('path/to/output2')

# Percentage difference for amplitude between two outputs from ARES
p_diff = o1.percent_diff(o2, 'amplitude')

# Mean squared error (MSE) between two outputs from ARES
mse = o1.mse(o2, 'fwhm')
```

## Columns available
These are the columns available from the ARES output:
* wavelength
* nlines
* depth
* fwhm
* EW
* EWerr
* amplitude
* sigma
* mean