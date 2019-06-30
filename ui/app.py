import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from backend.articles.newspaper import News
import urllib.request


class app():
    def __init__(self):
        app = QApplication(sys.argv)
        w = QWidget()

        self.news = News()
        w.setGeometry(100,100,1024,600)
        principal = QHBoxLayout()
        
        leftpart = QVBoxLayout()
        leftwidget = QWidget()
        leftwidget.setLayout(leftpart)
        leftwidget.setMaximumSize(200,600)
        search = QWidget()
        added = QWidget()
        addable = QWidget()
        configuration = QWidget()
        search_layout = QVBoxLayout()
        added_layout = QVBoxLayout()
        addable_layout = QVBoxLayout()
        configuration_layout= QVBoxLayout()
        search.setLayout(search_layout)
        
        sources = QWidget()
        sources_scroll = QScrollArea()
        sources_scroll.setWidget(sources)
        sources_layout = QVBoxLayout()
        sources_scroll.setWidgetResizable(True)
        sources.setLayout(sources_layout)
        added.setLayout(added_layout)
        addable.setLayout(addable_layout)
        configuration.setLayout(configuration_layout)
        self.sources = []
        try:
            r = open("save","r")
            d = r.readlines()
            self.sources = []
            for i in d:
                self.sources+=i.split("*")
        except:
            self.sources = []
        while '' in self.sources:
            self.sources.remove('')
        for i in self.sources:
            added_layout.addWidget(self.get_news_added(i))
        l = self.news.get_sources(self.sources)

        for i in l:
            addable_layout.addWidget(self.get_news_addable(i))
        search_bar_news = QLineEdit()
        search_bar_news.setText("Search for a newspaper")
        search_layout.addWidget(search_bar_news)

        pic_config = QLabel()
        pix_config = QPixmap("./resources/config.png")
        pix_config = pix_config.scaledToWidth(30)
        pix_config = pix_config.scaledToHeight(30)
        pic_config.setPixmap(pix_config)


        configuration_layout.addWidget(pic_config)
        leftpart.addWidget(search)
        sources_layout.addWidget(added)
        sources_layout.addWidget(addable)
        leftpart.addWidget(sources_scroll)
        leftpart.addWidget(configuration)
        leftwidget.setStyleSheet("background-color: #2c59a3;")

        rightpart = QVBoxLayout()
        rightwidget = QWidget()
        rightwidget.setLayout(rightpart)
        top_right = QWidget()
        top_right_layout = QHBoxLayout()
        top_right.setLayout(top_right_layout)
        
        search_article = QWidget()
        search_article_layout = QHBoxLayout()
        search_article.setLayout(search_article_layout)
        articles_scroll = QScrollArea()
        articles = QWidget()
        articles_scroll.setWidget(articles)
        articles_scroll.setWidgetResizable(True)
        articles_layout = QVBoxLayout()
        articles.setLayout(articles_layout)
        search_bar_article = QLineEdit()
        search_bar_article.setText("Search for an article")
        search_article_layout.addWidget(search_bar_article)

        
        pic = QLabel()
        pix = QPixmap("./resources/logo.png")
        pix = pix.scaledToWidth(300)
        pic.setPixmap(pix)
        
        for i in self.news.get_articles(self.sources):
            articles_layout.addWidget(self.get_article(i))
        top_right_layout.addStretch()
        top_right_layout.addWidget(pic)
        top_right_layout.addStretch()
        top_right_layout.addWidget(search_article)
        
        
        rightpart.addWidget(top_right)
        rightpart.addWidget(articles_scroll)
        rightpart.setAlignment(Qt.AlignTop)

        principal.addWidget(leftwidget)
        principal.addWidget(rightwidget)
        widget = QWidget()
        principal.setSpacing(0)
        w.setLayout(principal)
        w.setStyleSheet("padding:0px;background-color:white;")
        w.setWindowTitle("News Area")
        
        w.setWindowFlags(Qt.FramelessWindowHint)
        w.show()
        sys.exit(app.exec_())

    def get_news_added(self, param):
        w = QWidget()
        layout_w = QHBoxLayout()
        w.setLayout(layout_w)
        name = QLabel(param)
        button = QPushButton("-")
        button.clicked.connect(lambda:self.remove_paper(str(param)))
        button.setStyleSheet("background-color:red;color:white;")
        name.setStyleSheet("color:white;")
        layout_w.addWidget(name)
        layout_w.addStretch()
        layout_w.addWidget(button)
        w.setMaximumWidth(100)
        return w

    def remove_paper(self, param):
        self.sources.remove(param)
        print("SUPPRESSED ! ")
        self.save()

    def save(self):
        r = open("save","w")
        for i in self.sources:
            r.write(str(i)+"*")
        r.close()

    def get_news_addable(self, param):
        w = QWidget()
        layout_w = QHBoxLayout()
        w.setLayout(layout_w)
        name = QLabel(str(param))
        button = QPushButton("+")
        button.clicked.connect(lambda:self.add_paper(str(param)))
        button.setStyleSheet("background-color:green;color:white;")
        name.setStyleSheet("color:white;")
        layout_w.addWidget(name)
        layout_w.addStretch()
        layout_w.addWidget(button)
        w.setMaximumWidth(100)
        return w

    def add_paper(self, param):
        self.sources.append(param)
        print("ADDED")
        self.save()
        
    def get_article(self, param):
        w = QWidget()
        layout_w = QHBoxLayout()
        url = param.urlToImage
        data = urllib.request.urlopen(url).read()
        image = QImage()
        image.loadFromData(data)
        pic = QLabel()
        pix = QPixmap(image)
        pix = pix.scaledToWidth(100)
        pix = pix.scaledToHeight(100)
        pic.setPixmap(pix)

        middle_layout = QVBoxLayout()
        middle = QWidget()
        middle.setLayout(middle_layout)
        title = QLabel(param.title)
        print("Title : "+param.title)
        title.setStyleSheet("font-size:30px;color:black;")
        description = QLabel(param.description)
        print("Description :"+param.description)
        description.setStyleSheet("font-size:10px;color:black;")
        middle_layout.addWidget(title)
        middle_layout.addWidget(description)

        right_layout = QVBoxLayout()
        right = QWidget()
        right.setLayout(right_layout)
        objectivity_title = QLabel("Objectivity")
        objectivity = QLabel("88%")
        fake_title = QLabel("Fake Chance")
        fake = QLabel("2%")
        right_layout.addWidget(objectivity_title)
        right_layout.addWidget(objectivity)
        right_layout.addWidget(fake_title)
        right_layout.addWidget(fake)

        layout_w.addWidget(pic)
        layout_w.addWidget(middle)
        layout_w.addWidget(right)
        w.setLayout(layout_w)
        w.setMaximumWidth(650)
        w.setMaximumHeight(140)
        return w