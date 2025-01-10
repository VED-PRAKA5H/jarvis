from PyQt5.QtWidgets import *  # Import all classes from PyQt5's widgets module
from PyQt5.QtGui import *  # Import all classes from PyQt5's GUI module
from PyQt5.QtCore import Qt, QSize, QTimer  # Import specific classes from PyQt5's core module
from dotenv import load_dotenv  # Import the load_dotenv function to manage environment variables
import os  # Import the os module for operating system dependent functionality
import sys  # Import the sys module for system-specific parameters and functions

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variable for Assistant name
Assistantname = os.getenv('Assistantname')
old_chat_messages = ""  # Variable to store previous chat messages
temp_dir_path = "./Files"  # Path for temporary files
graphics_dir_path = "./Graphics"  # Path for graphic files

def answer_modifier(answer):
    """Removes empty lines from a given answer."""
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def query_modifier(query):
    """Modify the query to ensure it ends with appropriate punctuation."""
    new_query = query.lower().strip()
    question_words_list = ['how', 'what', 'who', 'where', 'why', 'which', 'can you', "what's", 'when',
                           'could you', 'would you', 'do you', 'is it', 'are you', 'has anyone',
                           'who is', 'what if', 'why don’t', 'how come', 'what time',
                           'how many', 'how much', 'how long', 'how often',
                           'what kind', 'what type', 'where can', 'whose',
                           'is there', 'what about', 'how does',
                           'where is', 'who are', 'what happened',
                           'can I', 'may I', 'should I',
                           'will you', 'can you tell me',
                           'what would', 'who could',
                           'what do', 'what should']

    if any(word + " " in new_query for word in question_words_list):
        new_query += "?"
    else:
        new_query += "."
    return new_query.capitalize()

def set_microphone_status(command):
    """Writes the microphone status to a file."""
    with open(f"{temp_dir_path}/Mic.data", 'w', encoding='utf-8') as file:
        file.write(command)

def get_microphone_status():
    """Reads the microphone status from a file."""
    try:
      with open(f"{temp_dir_path}/Mic.data", 'r', encoding='utf-8') as file:
          return file.read()
    except FileNotFoundError:
        return "False"  # Or some other default

def set_assistant_status(command):
    """Writes the assistant status to a file."""
    with open(f"{temp_dir_path}/Status.data", 'w', encoding='utf-8') as file:
        file.write(command)

def get_assistant_status():
  """Reads the assistant status from a file."""
  try:
    with open(f"{temp_dir_path}/Status.data", 'r', encoding='utf-8') as file:
        return file.read()
  except FileNotFoundError:
        return ""  # Or some other default

def mic_button_initialized():
    """Sets the microphone status to 'False'."""
    set_microphone_status("False")

def mic_button_closed():
    """Sets the microphone status to 'True'."""
    set_microphone_status('True')

def graphics_dirctory_path(file_name):
    """Generates the full path for a graphics file."""
    return f"{graphics_dir_path}/{file_name}"

def temp_directory_path(file_name):
    """Generates the full path for a temporary file."""
    return f"{temp_dir_path}/{file_name}"

def show_text_to_screen(text):
    """Writes text to a file, presumably for display on the screen."""
    with open(f"{temp_dir_path}/Responses.data", 'w', encoding='utf-8') as file:
        file.write(text)

class ChatSection(QWidget):
    """Sets up the main chat window."""
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        text_color = QColor(Qt.red)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)

        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(graphics_dirctory_path('Jarvis2.gif'))
        max_gif_size_w = 480
        max_gif_size_h = 270
        movie.setScaledSize(QSize(max_gif_size_w, max_gif_size_h))
        self.gif_label.setAlignment((Qt.AlignRight | Qt.AlignBottom))
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)

        self.label = QLabel('')
        self.label.setStyleSheet("color: white; font-size:16px; margin-right:195px; border:none;margin-top:-30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)

        font = QFont()
        font.setPointSize(14)
        self.chat_text_edit.setFont(font)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar:: handle: vertical {
                background: white;
                min-height: 20px;
            }
            QScrollBar:: add-line:vertical {
                background: black;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar:: sub-line:vertical {
                background: black;
                subcontrol-position: top;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar:: up-arrow: vertical, QScrollBar:: down-arrow:vertical {
                border: none;
                background: none;
                color: none;
            }
            QScrollBar:: add-page: vertical, QScrollBar:: sub-page:vertical {
                background: none;
            }
        """)

    def loadMessages(self):
        """Retrieves and displays new messages."""
        global old_chat_message
        try:
            with open(temp_directory_path('Responses.data'), "r", encoding="utf-8") as File:
                messages = File.read()
        except FileNotFoundError:
            messages = ""
        if not messages:
           pass
        elif str(old_chat_message) == str(messages):
            pass
        else:
            self.addMessage(message=messages, color='White')
            old_chat_message = messages

    def SpeechRecogText(self):
        """Updates the status label with the content of the 'Status.data' file."""
        try:
           with open(temp_directory_path('Status.data'), "r", encoding='utf-8') as file:
              messages = file.read()
        except FileNotFoundError:
            messages = ""
        self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        """Loads and sets an icon on the icon label."""
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
      """Toggles the microphone icon and status."""
      if self.toggled:
          self.load_icon(graphics_dirctory_path('voice.png'), 60, 60)
          mic_button_initialized()
      else:
          self.load_icon(graphics_dirctory_path('mic.png'), 68, 68)
          mic_button_closed()
      self.toggled = not self.toggled

    def addMessage(self, message, color):
       """Appends a message to the chat window with formatting."""
       cursor = self.chat_text_edit.textCursor()
       format = QTextCharFormat()
       formatm = QTextBlockFormat()
       formatm.setTopMargin(10)
       formatm.setLeftMargin(10)
       format.setForeground(QColor(color))
       cursor.setCharFormat(format)
       cursor.setBlockFormat(formatm)
       cursor.insertText(message + "\n")
       self.chat_text_edit.setTextCursor(cursor)


class InitialScreen(QWidget):
    """Sets up the initial screen with a GIF and a microphone icon."""
    def __init__(self, parent=None):
        super().__init__(parent)

        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        gif_label = QLabel()
        movie = QMovie(graphics_dirctory_path('Jarvis2.gif'))
        # Set background color to #030217
        self.setStyleSheet("background-color: #030217;")
        gif_label.setMovie(movie)
        gif_width = 800
        gif_height = 600
        movie.setScaledSize(QSize(gif_width-100, gif_height-100))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.icon_label = QLabel()
        pixmap = QPixmap(graphics_dirctory_path('Mic_on.png'))
        new_pixmap = pixmap.scaled(60, 60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        """Updates the status label with the content of the 'Status.data' file."""
        try:
           with open(temp_directory_path('Status.data'), "r", encoding='utf-8') as file:
              messages = file.read()
        except FileNotFoundError:
            messages = ""
        self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        """Loads and sets an icon on the icon label."""
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        """Toggles the microphone icon and status."""
        if self.toggled:
            self.load_icon(graphics_dirctory_path("Mic_on.png"), 60, 60)
            mic_button_initialized()
        else:
            self.load_icon(graphics_dirctory_path('Mic_off.png'), 60, 60)
            mic_button_closed()
        self.toggled = not self.toggled


class MessageScreen(QWidget):
    """Sets up the layout for the main chat screen."""
    def __init__(self, parent=None):
        super().__init__(parent)

        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)


class CustomTopBar(QWidget):
    """Creates a custom top bar for the application."""
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.current_screen = None
        self.initUI()

    def initUI(self):
        """Initializes the UI for the custom top bar."""
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        home_button = QPushButton()
        home_icon = QIcon(graphics_dirctory_path("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText(" Home")
        home_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color: black")
        message_button = QPushButton()
        message_icon = QIcon(graphics_dirctory_path("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText(" Chat")
        message_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color: black")
        minimize_button = QPushButton()
        minimize_icon = QIcon(graphics_dirctory_path("Minimize2.png"))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow)

        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(graphics_dirctory_path("Maximize.png"))
        self.restore_icon = QIcon(graphics_dirctory_path("Minimize.png"))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)

        close_button = QPushButton()
        close_icon = QIcon(graphics_dirctory_path("Close.png"))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.closeWindow)

        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")

        title_label = QLabel(f"{str(Assistantname).capitalize()} AI ")
        title_label.setStyleSheet("color: black; font-size: 18px; background-color:white")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)

        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        """Paints the background of the custom top bar."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        """Minimizes the main window."""
        self.parent().showMinimized()

    def maximizeWindow(self):
        """Maximizes or restores the main window."""
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        """Closes the main window."""
        self.parent().close()

    def mousePressEvent(self, event):
        """Handles mouse press events for dragging the window."""
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """Handles mouse move events for dragging the window."""
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
      """Shows the message screen."""
      if self.current_screen is not None:
          self.current_screen.hide()
      message_screen = MessageScreen(self)
      layout = self.parent().layout()
      if layout is not None:
         layout.addWidget(message_screen)
      self.current_screen = message_screen

    def showInitialScreen(self):
       """Shows the initial screen."""
       if self.current_screen is not None:
          self.current_screen.hide()
       initial_screen = InitialScreen(self)
       layout = self.parent().layout()
       if layout is not None:
          layout.addWidget(initial_screen)
       self.current_screen = initial_screen


class MainWindow(QMainWindow):
    """Sets up the main application window."""
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        """Initializes the UI for the main window."""
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)


def GraphicalUserInterface():
    """Initializes and runs the graphical user interface."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    GraphicalUserInterface()
