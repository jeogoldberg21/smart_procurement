try:
    from matplotlib import pyplot as plt
    from matplotlib.dates import MonthLocator, num2date, AutoDateLocator, AutoDateFormatter
    from matplotlib.ticker import FuncFormatter
    from pandas.plotting import deregister_matplotlib_converters
    print('SUCCESS: All matplotlib imports work')
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
