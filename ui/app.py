import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import urllib.request


class app():
    def __init__(self):
        app = QApplication(sys.argv)
        self.w = QWidget()
        self.w.setGeometry(100,100,1366,800)
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
        self.categories = []
        try:
            r = open("sources_save","r")
            d = r.readlines()
            self.sources = []
            for i in d:
                self.sources+=i.split("*")
        except:
            self.sources = []

        try:
            r = open("categories_save","r")
            d = r.readlines()
            self.categories = []
            for i in d:
                self.categories+=i.split("*")
        except:
            self.categories = []


        self.watch_later_list = []
        self.watch_later_articles = []

        while '' in self.sources:
            self.sources.remove('')
        while '' in self.categories:
            self.categories.remove('')

        for i in self.sources:
            added_layout.addWidget(self.get_news_added(i))
        fix = open('sources','r').read()
        self.all_sources = fix.split('*')
        while ' ' in self.all_sources:
            self.all_sources = self.all_sources.remove(' ')


        pix_logo = QPixmap("./resources/logo.png")
        pix_logo = pix_logo.scaledToWidth(40)
        pix_logo = pix_logo.scaledToHeight(40)
        pic_logo = QLabel()
        pic_logo.setPixmap(pix_logo)
        pic_logo.setAlignment(Qt.AlignTop)
        pic_logo.mouseReleaseEvent=lambda event:self.back_home()

        pic_config = QPushButton()
        pix_config = QPixmap("./resources/settings-work-tool.png")
        pix_config = pix_config.scaledToWidth(40)
        pix_config = pix_config.scaledToHeight(40)
        icon = QIcon(pix_config)
        pic_config.setIcon(icon)
        pic_config.clicked.connect(lambda:self.parameter_window())

        self.articles_recents = QVBoxLayout()
        self.articles_watch_later = QVBoxLayout()

        configuration_layout.addWidget(pic_config)
        #leftpart.addWidget(sources_scroll)
        leftpart.addWidget(pic_logo)
        leftpart.addStretch()
        recents = QPushButton()
        recents.setIcon(QIcon("./resources/time-machine.png"))
        recents.setMinimumHeight(60)
        recents.clicked.connect(lambda:self.recents())
        watch_later = QPushButton()
        watch_later.setIcon(QIcon("./resources/reading-glasses.png"))
        watch_later.setMinimumHeight(60)
        watch_later.clicked.connect(lambda:self.watch_later())
        leftpart.addWidget(recents)
        leftpart.addWidget(watch_later)
        leftpart.addStretch()
        leftpart.addWidget(configuration)
        leftwidget.setStyleSheet("background-color: white;color:black;")
        leftwidget.setMaximumWidth(80)
        rightpart = QVBoxLayout()
        rightwidget = QWidget()
        rightwidget.setLayout(rightpart)
        top_right = QWidget()
        top_right_layout = QHBoxLayout()
        top_right.setLayout(top_right_layout)
        
        search_article = QWidget()
        search_article_layout = QHBoxLayout()
        search_article.setLayout(search_article_layout)

        self.Stack = QStackedWidget()
        
        articles_scroll = QScrollArea()

        self.Stack.addWidget(articles_scroll)

        articles = QWidget()
        articles_scroll.setStyleSheet("border: 0px solid black;")
        articles_scroll.setWidget(articles)
        articles_scroll.setWidgetResizable(True)
        articles_scroll.setMaximumWidth(850)
        
        self.articles_layout = QVBoxLayout()
        articles.setMaximumWidth(850)
        articles.setLayout(self.articles_layout)
        self.search_bar_article = QLineEdit()
        self.search_bar_article.setText("Search")
        self.search_bar_article.setStyleSheet("color:#aeafb0;font-size:20;")
        self.search_bar_article.setMaximumWidth(100)
        search_article_layout.addWidget(self.search_bar_article)
        self.search_bar_article.textChanged.connect(lambda:self.search_articles())
        try:
            ll = open("number_articles","r")
            self.number_articles = int(ll.read())
        except:
            self.number_articles = 0
        import os
        directory = "./backend/articles/downloaded"
        lim = [x[0] for x in os.walk(directory)][1:]
        self.articles = []
        for j in lim:
            dic = {}
            art = j+'/'+'article'
            fil = open(art,'r')
            gr = fil.readlines()
            for b in gr[:6]:
                tmp = b.split(':')
                tmp[0]=tmp[0].replace('\n','')
                tmp[1]=tmp[1].replace('\n','')
                #print('splitted : '+str(tmp))
                dic[tmp[0]]=tmp[1]
            dic['content']=' '.join(gr[7:])
            dic['path']=j
            dic['category'] = dic['category'].replace('[','')
            dic['category'] = dic['category'].replace(']','')
            dic['category'] = dic['category'].replace("'",'')
            if dic["category"] in self.categories:
                self.articles.append(dic)
            #print('ARTICLE : '+str(dic))
        self.articles_widget = []
        for i in self.articles:
            k = self.get_article(i)
            self.articles_widget.append(k)
            self.articles_layout.addWidget(k)
            splitter = QSplitter(Qt.Vertical)
            self.articles_layout.addWidget(splitter)
        top_right_layout.addStretch()
        top_right_layout.addStretch()
        top_right_layout.addWidget(search_article)
        
        top_right.setStyleSheet("background-color:#f2f3f5;")
        rightpart.addWidget(top_right)
        rightpart.addWidget(self.Stack)
        rightpart.setAlignment(Qt.AlignTop)

        principal.addWidget(leftwidget)
        principal.addWidget(rightwidget)
        widget = QWidget()
        principal.setSpacing(0)
        self.w.setLayout(principal)
        self.w.setStyleSheet("padding:0px;background-color:white;")
        self.w.setWindowTitle("News Area")
        
        
        self.w.setWindowFlags(Qt.FramelessWindowHint)
        
        self.w.show()
        self.sources_to_save = {}
        self.categories_to_save = {}
        self.w.setGeometry(100,0,1000,600)
        self.w.setMaximumSize(1000, 600)
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

        
    def get_article(self, param):
        w = QWidget()
        #w.setStyleSheet("border:2px solid #aeafb0;")
        w.mouseReleaseEvent=lambda event:self.show_article(param)
        layout_w = QHBoxLayout()
        pic = QLabel()
        pix = QPixmap(param['path']+'/'+'image.jpg')
        pix.scaled(100, 100, Qt.KeepAspectRatio)
        pic.setPixmap(pix)
        pic.setMaximumHeight(240)
        pic.setMaximumWidth(200)
        
        middle_layout = QVBoxLayout()
        middle = QWidget()
        middle.setLayout(middle_layout)
        title = QLabel(param['title'])
        title.setWordWrap(True);
        title.setStyleSheet("font-size:24px;color:black;")
        font = QFont("Times", 15, QFont.Bold)
        title.setFont(font)
        description = QLabel(param['description'])
        #font = QFont("Calibri", 12)
        #description.setFont(font)
        description.setStyleSheet("font-size:12px;color:black;")
        description.setWordWrap(True);
        

        right_layout = QHBoxLayout()
        right = QWidget()
        
        right.setLayout(right_layout)
        if "0" in param['objectivity']:
            obj = "Objective"
        else:
            obj = "Subjective"
        objectivity = QLabel(str(obj))
        objectivity.setAlignment(Qt.AlignCenter)
        objectivity.setStyleSheet("font-size:16px;color:white;background-color:black;text-align:center;")
        fake = QLabel(param['fake'])
        fake.setStyleSheet("font-size:16px;color:white;background-color:black;text-align:center;")
        fake.setAlignment(Qt.AlignCenter)
        objectivity.setMaximumWidth(100)
        fake.setMaximumWidth(100)
        param['category'] = param['category'].replace("'","")
        param['category'] = param['category'].replace("[","")
        param['category'] = param['category'].replace("]","")
        category = QLabel(str(param['category']))
        category.setStyleSheet("font-size:12px;color:black;")

        right_layout.addWidget(category)
        right_layout.addWidget(objectivity)
        right_layout.addWidget(fake)
        
        #layout_w.addWidget(right)
        layout_w.addWidget(middle)
        layout_w.addWidget(pic)


        middle_layout.addWidget(right)
        middle_layout.addWidget(title)
        middle_layout.addWidget(description)
        
        

        w.setLayout(layout_w)
        w.setMaximumWidth(800)
        w.setMinimumWidth(800)
        w.setMaximumHeight(240)
        w.setMinimumHeight(240)
        
        return w

    def show_article(self, art):
        scrolla = QScrollArea()
        widget_article = QWidget()
        scrolla.setWidgetResizable(True)
        scrolla.setWidget(widget_article)
        label = QLabel(art['content'])
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-size:14px;color:black;font-family:Calibri;")
        title = QLabel(art['title'])
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:26px;color:black;font-family:Times;")
        fullscreen = QPushButton("Distraction Free")
        fullscreen.setStyleSheet("font-size:14px;color:black;")
        fullscreen.clicked.connect(lambda:self.distraction())
        self.article_layout = QVBoxLayout()
        widget_article.setLayout(self.article_layout)
        pic = QLabel()
        pix = QPixmap(art['path']+'/'+'image.jpg')
        pic.setPixmap(pix)
        watch_later_button = QPushButton()
        watch_later_button.setIcon(QIcon("./resources/reading-glasses.png"))
        watch_later_button.setStyleSheet("font-size:14px;color:black;")
        self.article_layout.addWidget(fullscreen)
        self.article_layout.addWidget(title)
        self.article_layout.addWidget(pic)
        self.article_layout.addWidget(label)
        self.article_layout.addWidget(watch_later_button)
        self.article_layout.addWidget(watch_later_button)
        
        widget_article.setMaximumWidth(700)

        idx = 0
        count = 0
        for i in self.articles:
            if i["title"]==art["title"]:
                idx = count
            count += 1
        k = self.get_article(self.articles[idx])
        self.articles_recents.addWidget(k)
        l = self.get_article(self.articles[idx])
        watch_later_button.clicked.connect(lambda:self.articles_watch_later.addWidget(l))

        self.Stack.addWidget(scrolla)
        self.Stack.setCurrentIndex(1)

    def back_home(self):
        self.Stack.setCurrentIndex(0)
        widget = self.Stack.widget(1);
        self.Stack.removeWidget(widget)

    def distraction(self):
        self.w.showFullScreen()
        exit = QPushButton("Exit FullScreen")
        exit.clicked.connect(lambda: self.w.showNormal())
        self.article_layout.addWidget(exit)

    def parameter_window(self):
        categories_names = [
    "POLITICS",
    "WELLNESS",
    "ENTERTAINMENT",
    "TRAVEL",
    "STYLE & BEAUTY",
    "PARENTING",
    "HEALTHY LIVING",
    "QUEER VOICES",
    "FOOD & DRINK",
    "BUSINESS",
    "COMEDY",
    "SPORTS",
    "BLACK VOICES",
    "HOME & LIVING",
    "PARENTS",
    "THE WORLDPOST",
    "WEDDINGS",
    "WOMEN",
    "IMPACT",
    "DIVORCE",
    "CRIME",
    "MEDIA",
    "WEIRD NEWS",
    "GREEN",
    "WORLDPOST",
    "RELIGION",
    "STYLE",
    "SCIENCE",
    "WORLD NEWS",
    "TASTE",
    "TECH",
    "MONEY",
    "ARTS",
    "FIFTY",
    "GOOD NEWS",
    "ARTS & CULTURE",
    "ENVIRONMENT",
    "COLLEGE",
    "LATINO VOICES"
    "CULTURE & ARTS",
    "EDUCATION",
]
        w = QWidget()
        wlists = QWidget()
        layout = QVBoxLayout()
        title_widget = QLabel()
        title_widget.setText("Notable")
        title_widget.setStyleSheet("font-size:26px;color:black;font-family:Times")
        description_widget = QLabel()
        description_widget.setText("Notable is an aggregator of articles. The application allows each user to select the feeds that interest him on the news sites and thus make his own magazine. Notable indicates the degree of subjectivity of an article and makes it possible to classify an article of presses according to whether it is an intox (fake news) being based on the objectivity of its author.")
        description_widget.setStyleSheet("color:black;font-family:Calibri;")
        description_widget.setMaximumWidth(600)
        description_widget.setWordWrap(True)
        

        check_block = QWidget()
        check_block_layout = QHBoxLayout()
        check_block.setLayout(check_block_layout)

        categories_scroll = QScrollArea()
        categories_scroll.setWidgetResizable(True)
        categories_scroll.setWidget(wlists)
        hbox = QVBoxLayout()
        wlists.setLayout(hbox)
        for i in categories_names:
            cat = QWidget()
            bbox = QHBoxLayout()
            cat.setLayout(bbox)
            lab = QLabel()
            lab.setText(str(i))
            lab.setStyleSheet("font-size:20px;color:black;font-family:Calibri;")
            check = QCheckBox()
            if i in self.categories:
                check.setChecked(True)
            self.categories_to_save[i]=check
            bbox.addWidget(lab)
            bbox.addWidget(check)
            hbox.addWidget(cat)


        sources_scroll = QScrollArea()
        sources_widget = QWidget()
        sources_layout = QVBoxLayout()
        sources_widget.setLayout(sources_layout)
        sources_scroll.setWidget(sources_widget)
        sources_scroll.setWidgetResizable(True)
        for i in self.all_sources:
            bbox = QHBoxLayout()
            wid = QWidget()
            wid.setLayout(bbox)
            lab = QLabel(str(i))
            lab.setStyleSheet("font-size:20px;color:black;font-family:Calibri")
            check = QCheckBox()
            self.sources_to_save[i]=check
            if i in self.sources:
                check.setChecked(True)
            bbox.addWidget(lab)
            bbox.addWidget(check)
            sources_layout.addWidget(wid)

        

        instances = QWidget()
        instances_layout = QHBoxLayout()
        instances.setLayout(instances_layout)
        lab_inst = QLabel("Number of saved articles ")
        lab_inst.setStyleSheet("color:black;font-family:Calibri;")
        self.input_inst = QSlider(Qt.Horizontal)
        self.input_inst.setMinimum(10)
        self.input_inst.setMaximum(1000)

        self.input_inst.setTickPosition(QSlider.TicksBelow)
        self.input_inst.setTickInterval(25)
        self.label_number = QLabel()
        self.label_number.setStyleSheet("color:black;")
        self.input_inst.valueChanged[int].connect(lambda:self.change_number())
        print(" number : "+str(self.number_articles))
        self.input_inst.setValue(self.number_articles)


        instances_layout.addWidget(lab_inst)
        instances_layout.addWidget(self.input_inst)
        instances_layout.addWidget(self.label_number)

        save = QPushButton("Save")
        save.clicked.connect(lambda:self.save_preferences())
        save.setStyleSheet("color:#f21512;")
        layout.addWidget(title_widget)
        layout.addWidget(description_widget)

        
       # sources_scroll.setFixedHeight(200)
        check_block_layout.addWidget(categories_scroll)
        check_block_layout.addWidget(sources_scroll)
        layout.addWidget(check_block)
        
        layout.addWidget(instances)
        
        layout.addWidget(save)
        w.setLayout(layout)
        self.Stack.addWidget(w)
        self.Stack.setCurrentIndex(1)

    def search_articles(self):
        s = str(self.search_bar_article.text())
        for i in reversed(range(self.articles_layout.count())): 
            self.articles_layout.itemAt(i).widget().setParent(None)
        for i in self.articles:
            if s.lower() in i["title"].lower() or s in i["description"].lower() or s.lower() in i["category"].lower() or s.lower() in i["content"].lower():
                k = self.get_article(i)        
                self.articles_widget.append(k)
                self.articles_layout.addWidget(k)
                splitter = QSplitter(Qt.Vertical)
                self.articles_layout.addWidget(splitter)

    
    def save_preferences(self):
        cat = open("categories_save","w")
        lcat = []
        sour = open("sources_save","w")
        lsour = []
        for i in self.categories_to_save:
            if self.categories_to_save[i].isChecked():
                lcat.append(i)

        for i in self.sources_to_save:
            if self.sources_to_save[i].isChecked():
                lsour.append(i)

        cat.write('*'.join(lcat))
        sour.write('*'.join(lsour))

        lom = open("number_articles","w")
        lom.write(str(self.input_inst.value()))
        lom.close()

        cat.close()
        sour.close()

    def change_number(self):
        self.label_number.setText(str(self.input_inst.value()))


    def watch_later(self):            
        w = QWidget()
        w.setLayout(self.articles_watch_later)
        self.Stack.addWidget(w)
        self.Stack.setCurrentIndex(1)

    def recents(self):
        w = QWidget()
        w.setLayout(self.articles_recents)
        self.Stack.addWidget(w)
        self.Stack.setCurrentIndex(1)