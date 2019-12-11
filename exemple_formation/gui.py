"""
Interface graphique wxPython

1. créer des éléments graphiques :
    - une fenêtre
    - des widgets
2. agencer / mettre en page (layout)
3. connecter des comportements à ces widgets : événements du framework -> fonctions définies par nous
4. passer la main à la boucle d'événements du framework
    - "Hollywood principle" : "don't call us, we'll call you"
"""

import wx
import wx.html

def main():
    app = wx.App()

    fenêtre = wx.Frame(None, title="Lecteur RSS")

    conteneur = wx.Panel(fenêtre)

    # A gauche, la liste des flux
    liste_flux = wx.ListBox(conteneur, choices=["Aaaaa", "Bbbbb", "Cccccc"])

    partie_droite = wx.Panel(conteneur)

    # À droite, en haut, la liste des articles
    liste_articles = wx.ListCtrl(partie_droite, style=wx.LC_REPORT)

    # À droite, en bas, le contenu de l'article
    contenu_article = wx.html.HtmlWindow(partie_droite)

    # Agencement de la partie droite : vertical un quart / trois quarts
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(liste_articles, proportion=1, flag=wx.EXPAND)
    sizer.Add(contenu_article, proportion=3, flag=wx.EXPAND)
    partie_droite.SetSizer(sizer)

    # Agencement principal : horizontal un tiers / deux tiers
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(liste_flux, proportion=1, flag=wx.EXPAND)
    sizer.Add(partie_droite, proportion=2, flag=wx.EXPAND)
    conteneur.SetSizer(sizer)

    fenêtre.Show()
    app.MainLoop()
