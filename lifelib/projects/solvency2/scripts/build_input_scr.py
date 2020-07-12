"""Module to import additional cells for SCR calculation from input file.

This module contains a function :py:func:`build_input_scr`,
which is called from :py:func:`~solvency2.solvency2.build`,
after :py:func:`~solvency2.build_input`
to create additional cells in ``Input`` space.

"""

def build_input_scr(space, input_file):
    """Create ``CorrLife`` and ``LifeFactors`` cells in ``Input`` space"""

    space.new_cells_from_excel(
            book=input_file,
            range_='CorrLife',
            names_row=0,
            param_cols=[0],
            names_col=0,
            param_rows=[1],
            param_order=[0, 1])
    
    space.new_cells_from_excel(
            book=input_file,
            range_='LifeFactors',
            names_row=0,
            param_cols=[0, 1, 2, 3])
    
    return space
