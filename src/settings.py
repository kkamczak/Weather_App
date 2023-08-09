SMALL_IMAGE_SIZE = (60, 60)
BIG_IMAGE_SIZE = (150, 150)

# FORECAST DATA---------------------------
HOUR_MIN = 12
HOUR_MAX = 16

TIMEOUT = 10

STYLE = """
    QWidget{
        background: #5e7572;
        background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #5e7572, stop: 1 #1c4d45);
        font-family: 'Calibri';
    }
    QLabel{
        background: none;
        color: #fff;
    }
    #label_main_image, #label_small_image_1, #label_small_image_2, #label_small_image_3, #label_small_image_4, #label_small_image_5{
        background: #5b9e96;
        border-radius: 25px;
        outline: none;
    }
    #label_Temperature, #label_Humidity, #label_Pressure, #label_Wind, #label_Sunrise, #label_Sunset, #label_Name{
        font-size: 16pt;
        font-weight: bold;
    }
    #label_error_message{
        font-size: 10pt;
        color: #77330d;
        text-align: center;
    }
    QLineEdit{
        padding: 1px;
        color: #000;
        border: 2px solid #fff;
        border-radius: 8px;
        background-color: #c3cdcc;
    }
    QPushButton{
        color: white;
        background: #048e7d;
        border: 5px #043832 solid;
        padding: 5px 10px;
        border-radius: 2px;
        font-weight: bold;
        font-size: 11pt;
        outline: none;
    }
    QPushButton:hover{
        border: 1px #C6C6C6;
        background: #0892D0;
    }
    QMenuBar:item{
        font-size: 12pt;
        color: white;
        background-color: #048e7d;
    }
    QMenuBar:item:selected{
        border: 1px #C6C6C6;
        background: #0892D0;
    }
    QMenu{
        font-size: 12pt;
        color: white;
        background-color: #048e7d;
    }
    QMenu:item:selected{
        border: 1px #C6C6C6;
        background: #0892D0;
    }
    QStatusBar{
        background: none;
    }
    QSizeGrip{
        background: none;
    }
    
"""

FRAMES_VARIABLES = [
    'label_small_date',
    'label_small_image',
    'label_small_temp',
    'label_small_weather'
]

CITIES = [
    "Paryż",
    "Florencja",
    "Barcelona",
    "Praga",
    "Kioto",
    "Wenecja",
    "Rzym",
    "Santorini",
    "Sydney",
    "Cape Town",
    "Vancouver",
    "San Francisco",
    "Rio de Janeiro",
    "Amsterdam",
    "Istanbul",
    "Edynburg",
    "Dubrownik",
    "Petra",
    "Buenos Aires",
    "Reykjavik",
    "Dubaj",
    "Singapur",
    "Queenstown",
    "Florencja"
]