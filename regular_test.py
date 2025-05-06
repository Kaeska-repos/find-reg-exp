import pytest
import wx
import re

from Regular import MainWindow


app = wx.App()
MainFrame = MainWindow()


@pytest.mark.parametrize("ignorecase, multiline, dotall, txt, regular, err_message", [
    (False, False, False, 'Find Russian letters: а, л, в.', '[алв]', 'Error when finding any regular expression.'), 
    (False, False, False, 'Google, Gooogle, Goooooogle', r'o{2,5}?', 'Error when finding any regular expression.'),
    (False, False, False, 'k1=1; k2 =2; k3 = 3', r'(k1|k2)\s*=\s*(\d+)', 'Error when finding capturing groups.'),
    (True, False, False, 'Find strings, string.', 'find', 'Error in the "ignorecase" checkbox.'),
    (False, True, False, 'Remember the phone numbers: 9876543210\n0123456789', r'\d{10}$', 'Error in the "multiline" checkbox.'),
    (False, False, True, 'first string\nlast string', 'first string.last string', 'Error in the "dotall" checkbox.'),
    ])
def test_regular(ignorecase, multiline, dotall, txt, regular, err_message):
    '''Checking for matches with the regular expression and the checkboxes.'''
    # Inserting values into the program window and getting the result.
    MainFrame.check_ignorecase.SetValue(ignorecase)
    MainFrame.check_multiline.SetValue(multiline)
    MainFrame.check_dotall.SetValue(dotall)
    MainFrame.text_ctrl.SetValue(txt)
    MainFrame.regular_ctrl.SetValue(regular)
    MainFrame.OnButton(wx.EVT_BUTTON)

    # Getting the result outside the graphical window.
    result = []
    flags = re.U
    if multiline:
        flags = flags|re.M
    if dotall:
        flags = flags|re.S
    if ignorecase:
        flags = flags|re.I
    for x in re.finditer(regular, txt, flags=flags):
        if not x.groups():
            result.append(x.group(0))
        else:
            result.append('     '.join(x.groups()))
    result = '\n'.join(result)
    assert MainFrame.result_ctrl.GetValue() == result, err_message