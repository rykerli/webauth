import sys
import requests
from lxml import html
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import configparser
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电信校园网认证")
        self.setGeometry(100, 100, 300, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        title_label = QLabel("电信校园网认证", central_widget)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 30px; font-weight: bold;")

        layout.addWidget(title_label)

        form_layout = QVBoxLayout()

        user_label = QLabel("学号", central_widget)
        user_label.setAlignment(Qt.AlignLeft)
        self.user_entry = QLineEdit(central_widget)
        self.user_entry.setPlaceholderText("请输入学号")

        password_label = QLabel("密码", central_widget)
        password_label.setAlignment(Qt.AlignLeft)
        self.password_entry = QLineEdit(central_widget)
        self.password_entry.setPlaceholderText("请输入密码")
        self.password_entry.setEchoMode(QLineEdit.Password)

        form_layout.addWidget(user_label)
        form_layout.addWidget(self.user_entry)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_entry)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        login_button = QPushButton("登录", central_widget)
        login_button.setFocusPolicy(Qt.NoFocus)
        login_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 20px;")
        login_button.clicked.connect(self.login)

        button_layout.addWidget(login_button)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)
        
        self.load_saved_credentials()
        
        self.user_entry.setTabOrder(self.user_entry, self.password_entry)
        self.password_entry.setTabOrder(self.password_entry, self.user_entry)
        
    def load_saved_credentials(self):
        config = configparser.ConfigParser()
    
        try:
            config.read('config.ini')
            username = config.get('Credentials', 'Username', fallback='')
            password = config.get('Credentials', 'Password', fallback='')
        
            self.user_entry.setText(username)
            self.password_entry.setText(password)
        except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError):
            pass

    def save_credentials(self):
        username = self.user_entry.text()
        password = self.password_entry.text()

        config = configparser.ConfigParser()
        config['Credentials'] = {'Username': username, 'Password': password}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)


    def login(self):
        username = self.user_entry.text()
        password = self.password_entry.text()

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            "loginType": "",
            "auth_type": "0",
            "isBindMac1": "0",
            "pageid": "1",
            "templatetype": "1",
            "listbindmac": "0",
            "recordmac": "0",
            "isRemind": "1",
            "loginTimes": "",
            "groupId": "",
            "distoken": "",
            "echostr": "",
            "url": "",
            "isautoauth": "",
            "notice_pic_loop2": "/portal/uploads/pc/demo2/images/bj.png",
            "notice_pic_loop1": "/portal/uploads/pc/demo2/images/logo.png",
            "userId": username,
            "passwd": password,
            "remInfo": "on"
        }

        try:
            url = "https://10.254.241.3/webauth.do?&wlanacname=SC-CD-XXGCDX-SR8810-X"
            response = requests.post(url, headers=headers, data=payload, verify=False)
            if response.status_code == 200:
                root = html.fromstring(response.content)
                self.save_credentials()

                element = root.xpath('//*[@id="goLoginForm"]/div[1]/div/div[2]/div[2]/div[5]/p')

                if element:
                    text_content = element[0].text_content().strip()
                    QMessageBox.information(self, "登录结果", text_content)
                else:
                    QMessageBox.critical(self, "登录失败", "未找到登录结果元素")
            else:
                QMessageBox.critical(self, "请求失败", f"状态码：{response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "请求异常", str(e))
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.login() 

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.login()       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = LoginWindow()
    main_window.show()
    sys.exit(app.exec_())
