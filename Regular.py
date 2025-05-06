'''This program finds all matches with the regular expression in the text_ctrl.
The text_ctrl and the regular expression are entered by the user. Author: KaeSKaterina.
'''


import wx
import re


class MainWindow(wx.Frame):
    '''This is the only program window.'''

    def __init__(self):
        super().__init__(None, title='Регулярные выражения', size=(1000, 750), pos=(0, 0))
        self.Maximize()

        # A section for creating widgets.
        main_pnl = wx.Panel(self)
        main_pnl.SetBackgroundColour('#cef')
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(13)
        main_pnl.SetFont(font)
        doc_lbl = wx.StaticText(main_pnl, label='Эта программа находит в тексте совпадения с регулярным выражением.')
        font.SetPointSize(16)
        main_pnl.SetFont(font)
        text_lbl = wx.StaticText(main_pnl, label='Введите текст:')
        self.text_ctrl = wx.TextCtrl(main_pnl, style=wx.TE_MULTILINE|wx.TE_RICH2)
        self.radio_rgb = wx.RadioBox(main_pnl, label='Цвет:', choices=['красный', 'зелёный', 'синий'])
        self.radio_rgb.SetBackgroundColour('#fff')
        self.radio_rgb.SetToolTip('Цвет, которым следует выделять найденные в тексте подстроки.')
        regular_lbl = wx.StaticText(main_pnl, label='Введите регулярное выражение:')
        self.regular_ctrl = wx.TextCtrl(main_pnl)
        self.check_ignorecase = wx.CheckBox(main_pnl, label='IGNORECASE')
        self.check_multiline = wx.CheckBox(main_pnl, label='MULTILINE')
        self.check_dotall = wx.CheckBox(main_pnl, label='DOTALL')
        result_lbl = wx.StaticText(main_pnl, label='Найденные соответствия:')
        self.result_ctrl = wx.TextCtrl(main_pnl, style=wx.CB_READONLY|wx.TE_MULTILINE)
        result_btn = wx.Button(main_pnl, label='Выполнить')

        # A section for placing widgets in sizers.
        border_sizer = wx.BoxSizer()  # Margins from the sides of the main window.
        main_pnl.SetSizer(border_sizer)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        border_sizer.Add(main_sizer, 1, wx.EXPAND|wx.ALL, 5)

        top_sizer = wx.GridBagSizer(5, 5)
        top_sizer.AddMany([
            (doc_lbl, (0, 0)),
            (text_lbl, (1, 0), (1, 1), wx.ALIGN_BOTTOM),
            (self.radio_rgb, (0, 1), (2, 1))
        ])
        top_sizer.AddGrowableCol(0, 1)

        flag_sizer = wx.BoxSizer()
        flag_sizer.AddMany([
            (self.check_dotall,),
            (self.check_ignorecase,),
            (self.check_multiline, 1),
            (result_btn,)
        ])
        
        main_sizer.AddMany([
            (top_sizer, 0, wx.EXPAND),
            (self.text_ctrl, 3, wx.EXPAND|wx.TOP, 5),
            (regular_lbl, 0, wx.TOP, 20),
            (self.regular_ctrl, 0, wx.EXPAND|wx.TOP, 5),
            (flag_sizer, 0, wx.EXPAND|wx.TOP, 5),
            (result_lbl, 0, wx.TOP, 20),
            (self.result_ctrl, 1, wx.EXPAND|wx.TOP, 5)
        ])

        # A section for describing event bindings.
        result_btn.Bind(wx.EVT_BUTTON, self.OnButton)


    # A section for describing function.
    def OnButton(self, event):
        '''Gets a result for searching for matches with a regular expression.'''
        result = []  # A variable for displaying the result as a list.
        result_hlight = []  # A variable for displaying the result as a text_ctrl color highlight.
        self.text_ctrl.SetStyle(0, len(self.text_ctrl.GetValue()), wx.TextAttr(wx.BLACK))
        # Getting the values of the flags and switches of the window.
        flags = re.U
        if self.check_multiline.GetValue():
            flags = flags|re.M
        if self.check_dotall.GetValue():
            flags = flags|re.S
        if self.check_ignorecase.GetValue():
            flags = flags|re.I
        rgb = self.radio_rgb.GetSelection()
        if rgb == 0:
            rgb = wx.RED
        elif rgb == 1:
            rgb = wx.GREEN
        else:
            rgb = wx.BLUE
        # Search for matches with a regular expression.
        for i in re.finditer(self.regular_ctrl.GetValue(), self.text_ctrl.GetValue(), flags=flags):
            result_hlight.extend([i.start(), i.end()])
            if not i.groups():  # If the expression does not contain a capturing group.
                result.append(i.group(0))
            else:
                result.append('     '.join(i.groups()))
        for i in range(0, len(result_hlight), 2):  # Highlighting of found matches.
            self.text_ctrl.SetStyle(result_hlight[i], result_hlight[i+1], wx.TextAttr(rgb))
        # Displaying the list.
        result = '\n'.join(result)
        self.result_ctrl.SetValue(result)

if __name__ == '__main__':
    app = wx.App()
    MainFrame = MainWindow()
    MainFrame.Show()
    app.MainLoop()