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

from exemple_formation.models import FluxRSS, init_db


def main():
    Session = init_db("exemple.db")
    db_session = Session()

    flux = db_session.query(FluxRSS).order_by("nom")

    app = wx.App()
    fenêtre = create_main_window(flux)
    app.MainLoop()


def create_main_window(titres_flux):
    fenêtre = MainWindow(titres_flux)
    fenêtre.Show()
    return fenêtre


class MainWindow(wx.Frame):
    def __init__(self, flux):
        super().__init__(None, title="Lecteur RSS")

        conteneur = wx.Panel(self)

        # A gauche, la liste des flux
        self.index_flux = dict(enumerate(flux))
        self.liste_flux = FeedList(
            conteneur,
            choices=[flux.nom for flux in flux],
            on_select=self.selection_flux,
        )

        partie_droite = wx.Panel(conteneur)

        # À droite, en haut, la liste des articles
        self.liste_articles = ArticleList(partie_droite)

        # À droite, en bas, le contenu de l'article
        self.contenu_article = ContenuArticle(partie_droite)

        # Agencement de la partie droite : vertical un quart / trois quarts
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.liste_articles, proportion=1, flag=wx.EXPAND)
        sizer.Add(self.contenu_article, proportion=3, flag=wx.EXPAND)
        partie_droite.SetSizer(sizer)

        # Agencement principal : horizontal un tiers / deux tiers
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.liste_flux, proportion=1, flag=wx.EXPAND)
        sizer.Add(partie_droite, proportion=2, flag=wx.EXPAND)
        conteneur.SetSizer(sizer)

    def selection_flux(self, event):
        flux = self.index_flux[event.GetSelection()]
        self.liste_articles.clear()
        self.liste_articles.add(flux.articles)


class FeedList(wx.ListBox):
    def __init__(self, *args, on_select=None, **kwargs):
        super().__init__(*args, **kwargs)
        if on_select is not None:
            self.Bind(wx.EVT_LISTBOX, on_select)


class ArticleList(wx.ListCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, style=wx.LC_REPORT, **kwargs)
        self.clear()

    def clear(self):
        self.ClearAll()
        self.init_colonnes()

    def init_colonnes(self):
        self.AppendColumn("Titre")
        self.AppendColumn("Date")

    def add(self, articles):
        for article in articles:
            self.Append((article.titre, article.date))


class ContenuArticle(wx.html.HtmlWindow):
    pass
