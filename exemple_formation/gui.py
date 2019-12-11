"""
Interface graphique wxPython

1. créer des élements graphiques :
    - une fenêtre
    - des widgets
2. agencer / mettre en page (layout)
3. connecter des comportements à ces widgets : événements du framework -> fonctions définies par nous
4. passer la main à la boucle d'événements du framework
    - "Hollywood principle" : "don't call us, we'll call you"
"""

import wx


def main():
    app = wx.App()
    fenêtre = wx.Frame(None, title="Lecteur RSS")
    fenêtre.Show()
    app.MainLoop()
