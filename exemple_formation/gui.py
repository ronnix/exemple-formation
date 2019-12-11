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

import os
import wx
import wx.html

from exemple_formation.models import Article, FluxRSS, init_db


def main():
    filename = os.path.join(os.getenv("APPDATA"), "flux.db")
    db_url = f"sqlite:///{filename}"
    Session = init_db(db_url)
    db_session = Session()

    flux = db_session.query(FluxRSS).order_by("nom")

    app = wx.App()
    fenêtre = create_main_window(db_session, flux)
    app.MainLoop()


def create_main_window(db_session, titres_flux):
    fenêtre = MainWindow(db_session, titres_flux)
    fenêtre.Show()
    return fenêtre


class MainWindow(wx.Frame):
    def __init__(self, db_session, flux):
        super().__init__(None, title="Lecteur RSS")

        self.db_session = db_session

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
        self.liste_articles = ArticleList(partie_droite, on_select=self.selection_article)

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
        self.contenu_article.clear()
        self.liste_articles.clear()
        self.liste_articles.add(flux.articles)

    def selection_article(self, event):
        article_id = event.GetData()
        article = self.db_session.query(Article).get(article_id)
        self.contenu_article.SetPage(article.contenu)


class FeedList(wx.ListBox):
    def __init__(self, *args, on_select=None, **kwargs):
        super().__init__(*args, **kwargs)
        if on_select is not None:
            self.Bind(wx.EVT_LISTBOX, on_select)


class ArticleList(wx.ListCtrl):
    def __init__(self, *args, on_select=None, **kwargs):
        super().__init__(*args, style=wx.LC_REPORT | wx.LC_SINGLE_SEL, **kwargs)
        if on_select is not None:
            self.Bind(wx.EVT_LIST_ITEM_SELECTED, on_select)
        self.clear()

    def clear(self):
        self.ClearAll()
        self.init_colonnes()

    def init_colonnes(self):
        self.AppendColumn("Titre")
        self.AppendColumn("Date")

    def add(self, articles):
        for index, article in enumerate(articles):
            self.Append((article.titre, article.date))
            self.SetItemData(index, article.id)


class ContenuArticle(wx.html.HtmlWindow):
    def clear(self):
        self.SetPage("")