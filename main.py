import sys
import requests
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QVBoxLayout
from PyQt5.QtCore import Qt #used for alignment
from PyQt5.QtWidgets import QPushButton
class WeatherApp(QWidget): #inherits from qwidget
    def __init__(self):
        super().__init__() #call the parent then the constructor
#creation
        self.city_label = QLabel("Enter city name: ",self)#just text
        self.city_input = QLineEdit(self)#can input
        self.get_weather_button = QPushButton("Get Weather",self)#button
        self.temperature_label = QLabel("",self)#just text
        self.emoji_label = QLabel(" ",self)#just text
        self.description_label = QLabel(self)#just text
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
#adding
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
#alignment
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        #QPushButton has no alignment

        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')

#creating a stylesheet
#syntax: class#id{""" """}
        self.setStyleSheet("""
             QLabel, QPushButton{
                font-family:'Calibri';
             }
              
             QLabel#city_label{
                  font-size: 40px;
                  font-weight: bold;
             }
             
             QLineEdit#city_input{
                  font-size: 20px;
             }
             
             QPushButton#get_weather_button{
                  font-size: 30px;
                  font-weight: bold;
             }
             
             QLabel#temperature_label{
                   font-size: 70px;
             }
             
             QLabel#emoji_label{
                   font-size: 100px;
                   font-family: Segoe UI;
             }
             
             QLabel#description_label{
                   font-size: 40px;
                   font-weight: bold;
             }
             
             """)
        self.get_weather_button.clicked.connect(self.get_weather)#with a signal of clicked we connect a slot of self.get_weather

    def get_weather(self):
        api_key = ""
        city = self.city_input.text()#.text to get the text
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()#will raise an exception if there are exceptions
            data = response.json()
            if data["cod"] != 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request")
                case 500:
                    self.display_error("Internal Server Error")
                case 404:
                    self.display_error("Not Found")
                case 401:
                    self.display_error("Unauthorized")#if api key is not valid
                case 403:
                    self.display_error("Forbidden")
                case 502:
                    self.display_error("Not Implemented")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error")
        except requests.exceptions.RequestException:
            self.display_error("Request Exception")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 70px")

        temperature = data["main"]["temp"] - 273.15
        weather_descr = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{temperature:.0f}°C")
        self.description_label.setText(weather_descr)
        self.emoji_label.setText(self.get_emoji(weather_id))


    @staticmethod
    #belong to a class,but don't require any instance specific data or any other methods,used more as a utility tool
    def get_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "🌩️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id < 741:
            return "💨"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🌬️"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""





if __name__ == "__main__": #if we run this directly,then we create a weather app object
    app = QApplication(sys.argv) #call the constructor from qapplication class;argv = arguments,sys.argv for sending arguments to the app
    weather_app = WeatherApp() #window
    weather_app.show() #if only .show is used then the window shows for a brief sec
    sys.exit(app.exec_())  #handles events

