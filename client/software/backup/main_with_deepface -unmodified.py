r'''The following code is used for testing miniconda.
It turns out if you follow the guideline of https://blog.arisa.moe/blog/2022/220429-dilb-ultimate-solution/#dlib, you do not have to use miniconda.
So now we quote this paragraph to make it a document but do not work.

import os

base_path = r"C:\Users\denti\miniconda3"
path = os.pathsep.join([os.path.join(base_path, i) for i in [r"",r"DLLs",r"Library\bin",r"pkgs\dlib-19.24.2-py38h314b149_2\Lib\site-packages"]])
os.environ["PATH"]+=os.pathsep+path
'''

## 单继承方法，能更好地进行界面与逻辑的分离
import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import Qt,QThread,QPointF,QPoint
from PyQt5.QtWidgets import QApplication, QGraphicsSceneHoverEvent, QMainWindow,QDialog,QFileDialog
from PyQt5.QtGui import QImage,QKeyEvent,QCursor
#from PyQt5.Qt import QStandardPaths
from cat import Ui_MainWindow
import cv2, imutils
import csv
from read_csv_Dialog import CustomUI as read_Dialog
from write_csv_Dialog import CustomUI as write_Dialog
import socket
from deepface import DeepFace
#import dlib
import os
import numpy as np
import matplotlib.pyplot as plt

from settings_Dialog import CustomUI as set_Dialog
from test_batch_detections import load_model,detect_face
#from emotion_detector import emotion_detector
import socketio
#from test_client import start_client
import json
import boto3
from bucket_test import upload_video,upload_video_new
#from math import floor
from json_handler import append_tojson,is_item_in_json,read_from_json
'''x= np.arange(1, 10, 1)
y=2*x'''

'''This is used to pause the main thread of the mainwindow while uploading the video.'''
class Thread(QThread):
    def __init__(self,s3_client,filename,bucket_name):
        super(Thread,self).__init__()
        self.s3_client=s3_client
        self.filename=filename
        self.bucket_name=bucket_name

    '''View file to know more information.'''
    def run(self):
        upload_video_new(self.s3_client,self.filename,'frank--bucket')

'''This is used to handle the situation when disconnection happens.'''
class disconnection__Thread(QThread):
    def __init__(self):
        super(disconnection__Thread,self).__init__()

    def run(self):
        #input('After the connection is recovered, press any key to resume: ')
        print('After the connection is recovered, everything is being recovered...now sending requests...')

class tabyy__Thread(QThread):
    def __init__(self):
        super(tabyy__Thread,self).__init__()

    def run(self):
        #input('After the connection is recovered, press any key to resume: ')
        input('Please check tabby...use ALT1 ALT2 ALT3 to start all the necessary pros. When everything is checked, press any key+enter to continue...')

'''This is the inner signal inside the point object. This is fired to refresh the displaying pane.'''
class inner_signal(QtCore.QObject):
    def __init__(self,parent=None):
        super().__init__(parent=None)

    mysignal=QtCore.pyqtSignal(str)

class MyItem(QtWidgets.QGraphicsEllipseItem): 
    def __init__(self,coordinates_dict,size):
        self.coordinates_dict=coordinates_dict
        self.size=size
        print(self.coordinates_dict['name'])
        super().__init__(self.coordinates_dict['center_x']-self.size/2,self.coordinates_dict['center_y']-self.size/2,self.size,self.size)
        #super().setPos(QtCore.QPointF(100,100))
        self.point_name=self.coordinates_dict['name']
        self.setToolTip(self.point_name)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setBrush(QtGui.QBrush(QtCore.Qt.yellow))
        self.setAcceptHoverEvents(True)

        self.set_ScaleCenter()

        self.inner_signal=inner_signal()
        
        print(self.get_dict())
        print("done")

    #mysignal=QtCore.pyqtSignal(str)


    def mouseReleaseEvent(self,event):
        print("uu")
        print(str(self.pos().x()))
        #self.mysignal.emit('refresh')
        self.inner_signal.mysignal.emit("refresh")
        return super().mouseReleaseEvent(event)
    
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        print("hovered.Now it is time to zoom.")
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.setFocus()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setScale(2.0)
        self.setOpacity(0.1)
        return super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        #print("hover out.Now it is time to go back to normal.")
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable,False)
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.setScale(1.0)
        self.setOpacity(1.0)
        #self.setToolTip(self.point_name)
        return super().hoverLeaveEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key()== Qt.Key_Up:
            #print("pressed")
            if self.flags() & QtWidgets.QGraphicsItem.ItemIsMovable:
                move_distance=QPointF(0,-5)
                self.moveBy(move_distance.x(),move_distance.y())
                cursor_pos=QCursor.pos()
                move_distancea=QPoint(0,-5)
                new_cursor_pos=cursor_pos+move_distancea
                QCursor.setPos(new_cursor_pos)

        if event.key()== Qt.Key_Down:
            #print("pressed")
            if self.flags() & QtWidgets.QGraphicsItem.ItemIsMovable:
                move_distance=QPointF(0,5)
                self.moveBy(move_distance.x(),move_distance.y())
                cursor_pos=QCursor.pos()
                move_distancea=QPoint(0,5)
                new_cursor_pos=cursor_pos+move_distancea
                QCursor.setPos(new_cursor_pos)

        if event.key()== Qt.Key_Left:
            print("pressed")
            if self.flags() & QtWidgets.QGraphicsItem.ItemIsMovable:
                move_distance=QPointF(-5,0)
                self.moveBy(move_distance.x(),move_distance.y())
                cursor_pos=QCursor.pos()
                move_distancea=QPoint(-5,0)
                new_cursor_pos=cursor_pos+move_distancea
                QCursor.setPos(new_cursor_pos)
                
        if event.key()== Qt.Key_Right:
            print("pressed")
            if self.flags() & QtWidgets.QGraphicsItem.ItemIsMovable:
                move_distance=QPointF(5,0)
                self.moveBy(move_distance.x(),move_distance.y())
                cursor_pos=QCursor.pos()
                move_distancea=QPoint(5,0)
                new_cursor_pos=cursor_pos+move_distancea
                QCursor.setPos(new_cursor_pos)
        return super().keyPressEvent(event)

    def get_dict(self): #get method,used with set method
        self.coordinates_dict['center_x']+=self.pos().x() #the "pos" method actually calculates within the self coordinates within the graphitems object. So actually it can be thought as a tracker.
        self.coordinates_dict['center_y']+=self.pos().y()
        #print(self.coordinates_dict)
        return self.coordinates_dict

    def set_position(self,center_x,center_y):  #the set method used to set new position. generated by co.
        x=center_x-(self.coordinates_dict['center_x'])
        y=center_y-(self.coordinates_dict['center_y'])
        self.setPos(x,y)  #no matter how you have toogles the point, it still remembers the original location.
        '''no need to do the following:
        self.coordinates_dict['center_x']=center_x
        self.coordinates_dict['center_y']=center_y
        the self.pos.x() and self.pos.y() will do their job.
        '''


    def set_ScaleCenter(self): #Since the default scale center is (0,0), you have to use this.
        self.setTransformOriginPoint(QtCore.QPointF(self.coordinates_dict['center_x'],self.coordinates_dict['center_y']))


class CustomUI(QMainWindow):
    '''The signal to change the progress bar. Because of the threads, you cannot change it directly.'''
    progressChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):

        #iheriting from QMainWndow
        super().__init__(parent) 

        #creating UI object.
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self) 

        #load the landmark list. This list is used to store Myitem objects.
        self.ui.landmark_list={}
        self.ui.landmark_size=10 #to do: changable size
        # load the dlib face shape predictor.
        #self.predictor = dlib.shape_predictor(os.path.abspath(os.path.join(os.getcwd(), ".."))+"\supporting_files\shape_predictor_68_face_landmarks\shape_predictor_68_face_landmarks.dat")

        # load the face detector.
        self.detector = load_model()
        self.detector.eval() #important

        self.model=DeepFace.build_model("Emotion")
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        #set the current frame that this program is working on.
        self.current_frame=0 #the 0th frame.
        self.slider_allow_auto_move=True

        #set the status to be needing analyze. In the loadImage() function, If a video is selected. The emotion degree will first be analyzed.
        self.requires_analyze=True

        self.landmarks=[]

        #In the load Image function, during the analysis process, this program will create a list storing happiness mark of all frames.
        self.emotion_mark_list=[]

        self.commissure_seq=[]

        self.nasion_list=[]

        self.conversion_list=[]

        self.leftx_eye_list=[]

        self.lefty_eye_list=[]

        self.conversion_factor_video=1

        self.display_tooth_landmarks=False

        self.save_img=False

        self.conversion_factor=0.33 #the factor used to measure distance(the distance of middle face.)[Now is the distance betwwen inner canthus.]

        self.incisor_edge_index=0.5

        self.cuspid_edge_index=0.5

        self.incisor_length=1.0

        self.Pause=False

        self.analyzed=False

        '''initialize the web client.'''

        self.ready=False
        '''This is the connection error handler that helps us to handle the situation when the internet disconnects when the program is just beginning to start.'''
        try:
            self.sio=self.start_client()
        
        except socketio.exceptions.ConnectionError:
            print('Not able to resume. Please check tabby if the connection is bulit then rerun this program. \nUse ALT 1,ALT2,ALT3 to start all the programs.\n start the  server first then connect the 5000 port.')
            '''
            Tabyy thread can not block the whole thread. So we change to the input method.
            This method will wait for the user input to continue.
            tThread=tabyy__Thread()
            tThread.start()
            tThread.wait()'''
            try:
                input('press any key + enter if you make sure the things above are all done.')
            except EOFError:
                pass
            self.sio=self.start_client()
            print('successfully bypassed this issue...')
        self.ready=True

        self.disconnected=False

        self.AI_dict={}

        #self.s3_resource = boto3.resource('s3')

        self.s3_client= boto3.client('s3')

        #to ensure the label in the column has enough width.
        self.ui.gridLayout.setColumnMinimumWidth(0,900)
        
        self.ui.pushButton.clicked.connect(self.pause)
        self.ui.pushButton_2.clicked.connect(self.my_slot)
        self.ui.pushButton_2.clicked.connect(self.loadImage)
        self.ui.pushButton_clear.clicked.connect(self.landmarks_clear)
        self.ui.pushButton_render.clicked.connect(self.landmarks_calculator)
        self.ui.pushButton_readcsv.clicked.connect(self.readcsv)
        self.ui.pushButton_writecsv.clicked.connect(self.writecsv)
        self.ui.slider_time.sliderReleased.connect(self.time_changed)
        self.ui.slider_time.sliderMoved.connect(self.overcome_zig)
        self.ui.time_setter.mysignal.connect(self.change_time)
        
        self.ui.lineEdit_media.textChanged.connect(self.media_monitor)

        self.ui.commandLinkButton.clicked.connect(self.open_settings)

        #creating a graphicsview to draw the landmark points.
        #setting the background to transparent so we can see the QLabel image.
        self.ui.graphicsView.setStyleSheet("background:transparent;")
        self.ui.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) #needed to keep the landmarks at correct place.
        self.ui.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) #since we do not need scroll bar in graphicsview. we need scrollbars in the outside of this widget.
        #since the first column has enough width, the width of the pixmap is accurate.
        self.ui.graphicsView.setGeometry(QtCore.QRect(95, 29, self.ui.label.pixmap().width(),self.ui.label.pixmap().height())) # set the size policy to preferred!!! default is expanding, which can leave a blank margin.
        self.ui.scene= QtWidgets.QGraphicsScene()
        
        self.ui.graphicsView.setScene(self.ui.scene)
        self.ui.graphicsView.scene().setSceneRect(-200, -200, 400, 400) #the value can be any value, but keep it to be (-x,-x,2x,2x),So the (0,0) point is in the correct place.

        #print(self.ui.label.pixmap().rect())

        #set the 'pause' botton to not enabled.
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_render.setEnabled(False)
        self.initial_state()
        self.tmp=None

        self.coord_offset=(0,0)
        #self.ui.label.setGeometry(QtCore.QRect(95, 29, 1000,618))
        #print(self.ui.label.parent.)

        '''https://cloud.tencent.com/developer/ask/sof/327869'''
        self.progressChanged.connect(self.ui.progressBar.setValue)

    def start_client(self,arg=None):
        pass
        sio = socketio.Client()

        sio.connect('http://localhost:5000')

        @sio.on('image_evaluated')
        def image_verified(data):
            print(float(data['happiness value']))

        '''internet progress bar'''
        @sio.on('video_analyzing')
        def move_progress_bar(data:str):
            self.current_frame=int(data)
            self.progressChanged.emit((self.current_frame/self.total_frame)*100)
            #self.ui.progressBar.setValue()

        @sio.on('send_list')
        def send_list(data):
            print(type(json.loads(data)))

        @sio.on('emotion_list_of_video')
        def recv_emotion_list(data):
            self.AI_dict=json.loads(data)
            self.emotion_mark_list=self.AI_dict['emotion_list']
            self.commissure_seq=self.AI_dict['commissure_list']
            print("c:"+str(len(self.commissure_seq)))
            self.face_not_detected=self.AI_dict['face_not_detected']
            self.face_greater_than_one_cv2_only=self.AI_dict['face_greater_than_one_cv2_only']
            self.face_greater_than_one_mobile=self.AI_dict['face_greater_than_one_mobile']
            #self.dlib_only_emotion_list=self.AI_dict['dlib_only_emotion_list']
            #print(self.dlib_only_emotion_list)
            '''We need to document the commissure seq.'''
            self.nasion_list=self.AI_dict['nasion_list']
            self.conversion_list=self.AI_dict['conversion_list']
            self.leftx_eye_list=self.AI_dict['leftx_eye_list']
            self.lefty_eye_list=self.AI_dict['lefty_eye_list']
            '''with open('commissure_list.json','a') as f:  #追加模式
                json.dump({'filename':self.media_source,
                           'fps':self.fps,
                           'emotion_mark_list':self.emotion_mark_list,
                           'commissure_seq':self.commissure_seq,
                           'nasion_list':self.nasion_list,
                           'conversion_list':self.conversion_list,
                           'leftx_eye_list':self.leftx_eye_list,
                           'lefty_eye_list':self.lefty_eye_list
                           },f) '''
            export_data={'filename':self.media_source,
                           'fps':self.fps,
                           'emotion_mark_list':self.emotion_mark_list,
                           'commissure_seq':self.commissure_seq,
                           'nasion_list':self.nasion_list,
                           'conversion_list':self.conversion_list,
                           'leftx_eye_list':self.leftx_eye_list,
                           'lefty_eye_list':self.lefty_eye_list
                           }
            self.process_seq_func()            
            self.requires_analyze=False
            self.ui.pushButton.setEnabled(True) #now you can press the pause button.
            self.ui.pushButton_2.setEnabled(False)
            self.display()
            self.mp4_state()
            print(json.loads(data)['name'])
            print(json.loads(data)['emotion_list'])
            print('not detected rate: '+str(self.face_not_detected/len(self.emotion_mark_list)))
            print('detected greater than one rate with cv2: '+str(self.face_greater_than_one_cv2_only/len(self.emotion_mark_list)))
            print('detected greater than one rate with mobile: '+str(self.face_greater_than_one_mobile/len(self.emotion_mark_list)))
            append_tojson('test.json',export_data)   #not too early. 
            
        
        @sio.event
        def disconnect():  #You don't have to manully use the disconnection, since it will disconnect automatically when the program returns.
            #sio.connect('http://localhost:5000')
            '''In the case we meet the disconnection(typically the ssh refusion error.)'''
            self.disconnected=True
            print("I'm disconnected!")

        @sio.event
        def connect():
            if self.disconnected==True and self.ready==True:
                try:
                    DThread=disconnection__Thread()
                    DThread.start()
                    DThread.wait()
                    sio.emit('How s it going',{'filename':self.media_source})
                    #print('detecting...waiting for connection')
                    self.disconnected=False

                except:
                    raise Exception('please check the connect function. Some error is not catched.')


        return sio

    def media_monitor(self):
        if self.ui.lineEdit_media.text()=='':
            self.ui.pushButton_2.setText('import new media')
            self.requires_analyze=True
            self.analyzed=False  #important
            '''self.vid.release()
            del self.vid
            importlib.reload(cv2)'''
            self.current_frame=0
            self.initial_state()
        else:
            pass

    def my_slot(self): #test function used to test slot.
        #self.ui.pushButton.setText("oo")
        pass
    
    '''The pause function works with pause button.
    '''
    def pause(self):
        self.ui.pushButton.setEnabled(False)#Once the pause button is hit, you cannot hit it twice unless you hit start.
        if self.current_frame<self.total_frame:
            self.Pause=True
        self.ui.time_setter.setText(str(float(self.current_frame/self.fps))) #time setter is the line edit next to the horizontal sliding bar. it displays current time.
        self.ui.pushButton_2.setEnabled(True)#When the pause button is hit, you can hit the start button.

    '''When you change the value of time setter and right click, the change_time function works to change the value of the horizontal sliding bar.
    It calculates the frame that needs to be calculated and bring it there by setting self.current_frame.
    It also reads that frame and renders it to the label by self.update()
    '''
    def change_time(self):
        self.ui.slider_time.setValue(int(float(self.ui.time_setter.text())/(self.total_frame/self.fps)*10000)) 

        frame_target=int(float(self.ui.time_setter.text())*self.fps)

        self.current_frame=frame_target

        if self.vid.isOpened():
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_target)
        
        self.ui.time_setter.setText(str(float(self.current_frame/self.fps)))

        img, self.image = self.vid.read()

        self.image  = imutils.resize(self.image ,height = 618 )

        self.update()
    
    '''only the import_media can be used.'''
    def initial_state(self):
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_render.setEnabled(False)
        self.ui.pushButton_readcsv.setEnabled(False)
        self.ui.pushButton_writecsv.setEnabled(False)
        self.ui.pushButton_clear.setEnabled(False)

    def mp4_state(self):
        self.ui.pushButton_render.setEnabled(True)
        self.ui.pushButton_readcsv.setEnabled(True)
        self.ui.pushButton_writecsv.setEnabled(True)
        self.ui.pushButton_clear.setEnabled(True)

    def pic_state(self):
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_render.setEnabled(True)
        self.ui.pushButton_readcsv.setEnabled(True)
        self.ui.pushButton_writecsv.setEnabled(True)
        self.ui.pushButton_clear.setEnabled(True)
    '''This load_local_image function is used for the testing of loadimage function.
    '''
    def load_local_image(self):
        local_img=cv2.imread('OIP-C-original.jpg')
        frame = cv2.cvtColor(local_img, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(image)) 
        self.ui.graphicsView.setGeometry(QtCore.QRect(95, 29, self.ui.label.pixmap().width(),self.ui.label.pixmap().height())) # set the size policy to preferred!!!  
        #everything done locally.
    
    def send_signal(self,data):
        self.progressChanged.emit(data)

    def loadImage(self):
        self.fps=25

        
        """ This function will load the camera device, obtain the image
            and set it to label using the setPhoto function.
            This works as the most important function of the whole program.
            First, it connects with the import media button.
            If you hit it, it will opens up a dialog to let you choose mp4 or jpg media.
            Before it processes the media, it filters the path you enter in the dialog.
            Filter 1: If you enter nothing, it will return None. Nothing will happen.
        """
        '''Below is the IP filter
        '''
        if self.ui.lineEdit_media.text()=='':
            self.media=QFileDialog.getOpenFileName(self,"choose media","C:/","(*.jpg;*.mp4)")
            self.media_source=str(self.media[0])
            self.ui.lineEdit_media.setText(self.media_source)

        if self.media_source=='':
            return
        
        if os.path.splitext(self.media_source)[-1]=='.jpg':
            self.pic_state()
            image = cv2.imdecode(np.fromfile(self.media_source, dtype=np.uint8), cv2.IMREAD_COLOR)
            #image=cv2.imread(self.media_source)
            
            #self.ui.label.setGeometry(QtCore.QRect(95, 29, image.shape[0],image.shape[1]))
            image,width,height=self.setPhoto_with_proper_height(image)
            self.image=image
            self.ui.graphicsView.setGeometry(QtCore.QRect(95, 29, width,height))
            print(width,height)

            #self.ui.pushButton_render.setEnabled(True) #after loading the image, the render button can be pushed.
            return

        '''Processing the video, either from real-time recording or local mp4.
        '''
        
        #cam = False # True for webcam

        #self.ui.graphicsView.setGeometry(QtCore.QRect(95, 29, 640,480)) # set the size policy to preferred!!!
        
        if not self.media_source=='':
            try:
                if self.analyzed==False:
                    self.vid = cv2.VideoCapture(self.media_source)
                    print("ready to capture new file.")
                    thread=Thread(self.s3_client,self.media_source,'frank--bucket')
                    thread.start()
                    thread.wait()
                    #upload_video_new(self.s3_resource,self.media_source,'frank--bucket',)
                else:
                    self.vid = cv2.VideoCapture("myvideo.mp4")
                    #upload_video(self.s3_resource,"myvideo.mp4",'frank--bucket',)
                self.vid.set(cv2.CAP_PROP_FPS, self.vid.get(cv2.CAP_PROP_FPS)/2)
                self.ui.pushButton_2.setText("start")
            except:
                return
        else:
            return
        
        self.total_frame=int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps=int(self.vid.get(cv2.CAP_PROP_FPS))
        self.video_duration=self.total_frame/self.fps

        if not self.current_frame<self.total_frame:
            self.current_frame=0

        print(self.current_frame)
        print(self.requires_analyze)

        self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        
        cnt=0
        frames_to_count=20
        st = 0
        fps=0
        
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

        if self.requires_analyze==True:
            self.ui.pushButton_2.setEnabled(False) #you cannot press the start button when it is analyzing.
            if is_item_in_json('test.json',self.media_source)==True:
                print('I noticed your mp4 being analyzed is in the test.json file,please decide whether you need it to be analyzed.')
                temp_data=read_from_json('test.json',self.media_source)
                self.media_source=temp_data['filename']
                self.fps=temp_data['fps']
                self.emotion_mark_list=temp_data['emotion_mark_list']
                self.commissure_seq=temp_data['commissure_seq']
                self.nasion_list=temp_data['nasion_list']
                self.conversion_list=temp_data['conversion_list']
                self.leftx_eye_list=temp_data['leftx_eye_list']
                self.lefty_eye_list=temp_data['lefty_eye_list']
                #self.process_seq_func()
                self.progressChanged.emit(100)  #In case the network failure.
        

                self.analyzed=True

                self.vid=cv2.VideoCapture("myvideo.mp4")
                self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)  #set to the first frame.
                self.total_frame=int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
                self.fps=int(self.vid.get(cv2.CAP_PROP_FPS))
                self.current_frame=0

                
                self.ui.graphicsView.setGeometry(QtCore.QRect(95, 29, self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)/self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)*618,618)) #change the graphicsview size when the analyzing has finished.

                self.requires_analyze=False
                self.ui.pushButton.setEnabled(True) #now you can press the pause button.
                self.ui.pushButton_2.setEnabled(False)
                self.display()
                self.mp4_state()
            else:
                self.analyze()
        else:
            self.ui.pushButton.setEnabled(True) #now you can press the pause button.
            self.ui.pushButton_2.setEnabled(False)
            self.display()
             #meaninng it has finished analyzing.
        
        
    def analyze(self):
        '''new function. save the video. to filter the emotion.'''
        #height=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        try:
            self.sio.call('analyze_uploaded_video_and_generate_emotion_list',{'filename':self.media_source},timeout=5)
        except:
            pass

        self.vid_writer=cv2.VideoWriter("myvideo.mp4",cv2.VideoWriter.fourcc('m','p','4','v'),self.fps,(int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        '''displaying the first frame.'''
        self.current_frame=0

        self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)

        print(self.total_frame)
        print(self.media_source)
        print(self.vid)

        img,self.image=self.vid.read()
        self.image  = imutils.resize(self.image ,height = 618 )
        self.ui.graphicsView.setGeometry(QtCore.QRect(95, 29, self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)/self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)*618,618)) #change the graphicsview size when the analyzing has finished.

        if self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)/self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)*618>1351-50:

            self.ui.gridLayout.setGeometry(QtCore.QRect(95, 29, 1351+200, 891))

        self.requires_analyze=False
        self.update()
        self.requires_analyze=True

        self.current_frame=0

        self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)


        '''
        while(self.vid.isOpened()):
            QtWidgets.QApplication.processEvents()	
            img, self.image = self.vid.read()
            if self.image is None: #None means the video has reached its end.
                break 
            #self.image  = imutils.resize(self.image ,height = 480 )
            #if self.slider_allow_auto_move==True:
            #    self.ui.slider_time.setValue(self.current_frame/self.total_frame*10000)
            re=self.process_with_AI()
            if re==None:
                self.emotion_mark_list.append(0)
            else:
                if re[2]==None:
                    pass
                else:
                    self.emotion_mark_list.append(re[2])
                    print("added")
                    self.vid_writer.write(self.image)

            #self.update()

            self.current_frame+=1

            self.ui.progressBar.setValue((self.current_frame/self.total_frame)*100)'''

            #key = cv2.waitKey(1) & 0xFF
            #if key == ord("q") or self.pause==True:
            #    self.pause=False
            #    break
    
    def process_seq_func(self):
        self.draw_align_point=False
        self.conver_accord_karmen=False
        self.draw_align_rect=False
        self.store_not_happy_frame_but_show=True  #another video that labels all not happy frames with a green frame.

        self.current_frame=0
        self.conversion_list_index=0

        #self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)

        #plt.plot(np.arange(0,len(self.emotion_mark_list)/self.fps,0.04), self.emotion_mark_list, 'g--')
        #与下面设置是一样的
        #plt.plot(x, y, linestyle='--', color='g')
        #plt.show()
        
        #plt.savefig("emotion.png")

        #self.commissure_seq=self.commissure_seq[0:len(self.commissure_seq)-1:2] #hotfix
        self.commissure_seq_temp=[]
        self.emotion_mark_list_temp=[]
        self.nasion_list_temp=[]

        if self.store_not_happy_frame_but_show==True:  #another video that labels all not happy frames with a green frame.
            self.vid_writer_another=cv2.VideoWriter("myvideo_another.mp4",cv2.VideoWriter.fourcc('m','p','4','v'),self.fps,(int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        while(self.vid.isOpened()):
            img, self.image = self.vid.read()
            if self.image is None:  ##not == None
                break
            self.image  = imutils.resize(self.image ,height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)) )
            print(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)) #necessary
            print(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  #necessary
            
            if self.store_not_happy_frame_but_show==True:  #another video that labels all not happy frames with a green frame.
                img_another=self.image
                if self.emotion_mark_list[self.current_frame]>0.9:
                    cv2.rectangle(img_another,(0,0),(img_another.shape[1],img_another.shape[0]),(0, 255, 0),2)
                self.vid_writer_another.write(img_another)

            if self.commissure_seq[self.current_frame]!=0:
                if self.draw_align_point==True:
                    cv2.circle(self.image,(round(self.leftx_eye_list[self.conversion_list_index]),round(self.lefty_eye_list[self.conversion_list_index])),8,(0, 255, 0),-1)
                if self.conver_accord_karmen==True: #if set to karmen filter,the video will change its size, which reduces the error caused by movements, however if the person do not move, it will cause extra error.
                    self.conversion_factor_video=self.conversion_list[self.conversion_list_index]
                else:
                    self.conversion_factor_video=1 #if the person is relatively static, please set to this.
                resized_img=cv2.resize(self.image,None,fx=self.conversion_factor_video,fy=self.conversion_factor_video)  #important
                new_img=np.ones_like(self.image)
                start_x=round((1-self.conversion_factor_video)*self.leftx_eye_list[self.conversion_list_index])
                start_y=round((1-self.conversion_factor_video)*self.lefty_eye_list[self.conversion_list_index])
                new_img[start_y:start_y+resized_img.shape[0],start_x:start_x+resized_img.shape[1]]=resized_img
                if self.draw_align_rect==True:
                    cv2.rectangle(new_img,(start_x,start_y),(start_x+resized_img.shape[1],start_y+resized_img.shape[0]),(0, 255, 0),2)

                self.vid_writer.write(new_img)
                self.commissure_seq_temp.append(self.commissure_seq[self.current_frame]*self.conversion_factor_video)  #important, we need to multiply conversion factor once since we assume it is in one dimension.
                self.emotion_mark_list_temp.append(self.emotion_mark_list[self.current_frame])
                self.nasion_list_temp.append(self.nasion_list[self.current_frame])
                self.conversion_list_index+=1
            self.current_frame+=1
            '''if self.image is None: 
                break'''
        if self.store_not_happy_frame_but_show==True:  #another video that labels all not happy frames with a green frame.
            self.vid_writer_another.release()

        '''to be done next'''
        self.vid_writer.release()
        
        
        self.commissure_seq=self.commissure_seq_temp
        self.emotion_mark_list=self.emotion_mark_list_temp
        self.nasion_list=self.nasion_list_temp    

        y=self.commissure_seq

        pre_x=np.arange(0,len(self.commissure_seq)/self.fps,1/self.fps)

        #z=[ii*30 for ii in self.conversion_list]

        #print("conversion_list:"+str(z))

        x=list(pre_x)

        plt.plot(x, y, 'g--') #hotfix

        #plt.plot(x,z)

        ymax = max(y)
        print(ymax)
        
        xpos = np.where(np.array(y) == ymax)
        print(xpos)
        for i in xpos[0]:
            print(x[i]) #the time of the largest nad biggest smile.

            plt.annotate('local max\n'+str(round(x[i],2)), xy=(x[i], ymax), xytext=(0, 0), textcoords='offset points')
        

        plt.savefig("commissure.png")

        plt.cla()

        self.progressChanged.emit(100)  #In case the network failure.
        

        self.analyzed=True

        self.vid=cv2.VideoCapture("myvideo.mp4")
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)  #set to the first frame.
        self.total_frame=int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps=int(self.vid.get(cv2.CAP_PROP_FPS))
        self.current_frame=0
        self.conversion_list_index=0
    
    def display(self):

        while(self.vid.isOpened()):
            QtWidgets.QApplication.processEvents()	
            img, self.image = self.vid.read()
            cv2.waitKey(33)
            if self.current_frame==self.total_frame-1: #None means the video has reached its end.
                self.current_frame=0
                self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
                self.ui.pushButton.click() #hit the pause button by itself.
            self.image  = imutils.resize(self.image ,height = 618 ) #to display more clearly.
            if self.slider_allow_auto_move==True:
                self.ui.slider_time.setValue(self.current_frame/self.total_frame*10000)

            #self.emotion_mark_list.append(self.process_with_AI()[2])
            '''new function.'''
            try:
                self.ui.verticalSlider.setValue(self.commissure_seq[self.current_frame]) #set the value to the possibility of happiness.
                self.ui.verticalSlider.setToolTip(str(self.commissure_seq[self.current_frame])) #use tooltip so you can visualize the current possibility.
            except:
                pass
            '''
            if self.emotion_mark_list[self.current_frame]>0.5:
                self.ui.verticalSlider.setValue(self.emotion_mark_list[self.current_frame]*100) #set the value to the possibility of happiness.
                self.ui.verticalSlider.setToolTip(str(self.emotion_mark_list[self.current_frame]*100)) #use tooltip so you can visualize the current possibility.
            else:
                self.ui.verticalSlider.setValue(0)
                self.ui.verticalSlider.setToolTip(str(self.emotion_mark_list[self.current_frame]*100)) #use tooltip so you can visualize the current possibility.
            '''

            self.update()

            self.current_frame+=1

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or self.Pause==True: #detect the pause
                self.Pause=False
                self.ui.pushButton_2.setEnabled(True)
                break

    '''
    def process_with_AI(self): #process self.image

        emotion_idx,preds,happiness_value=emotion_detector(self.image,self.face_cascade,self.model)

        if happiness_value>0.9:
            landmarks = detect_face(self.detector,self.image)
            if landmarks!=None:
                #now we are writing a function to analyze the distance between commissures.
                #
                # 遍历每一个检测到的人脸
                #transformed_landmarks_dict_list=[]
                #if len(faceb)==1: #表示探测到了人脸
                    # 获取关键点
                self.landmarks=landmarks
                print(self.mol_of_vec((landmarks[48][0],landmarks[48][1]),(landmarks[54][0],landmarks[54][1])))
                print(happiness_value)
                self.commissure_seq.append(self.mol_of_vec((landmarks[48][0],landmarks[48][1]),(landmarks[54][0],landmarks[54][1])))
                return [emotion_idx,preds,happiness_value]
            else:
                return None
        else:
            #self.commissure_seq.append(0)
            return None
    '''            

    def setPhoto(self,image):
        """ This function will take image input and resize it 
            only for display purpose and convert it to QImage
            to set at the label.
        """
        self.tmp = image
        if self.requires_analyze==True:
            image = imutils.resize(image,width=640)
        else:
            image= imutils.resize(image,height=618)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def setPhoto_with_proper_height(self,image):
        """ This function will take image input and resize it 
            only for display purpose and convert it to QImage
            to set at the label.
        """
        self.tmp = image
        image = imutils.resize(image,height=618)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(image))
        return(frame,frame.shape[1],frame.shape[0])
        

    def update(self):
        self.setPhoto(self.image)

    def landmarks_clear(self):
        self.ui.scene.clear()
        #self.ui.graphicsView.setScene(self.ui.scene)
        self.ui.landmark_list.clear() #if delete this,there will be a RuntimeError: wrapped C/C++ object of type QGraphicsRectItem has been deleted.

        print(self.ui.scene) #you do not have to createa new scene.

    def landmarks_calculator(self):
        # 检测人脸
        landmarks=detect_face(self.detector,self.image)
        transformed_landmarks_dict_list=[]
        if landmarks!=None:
            self.landmarks=landmarks
            #print('left_eye_x='+str(landmarks.part(36).x),'left_eye_y='+str(landmarks.part(36).y))
            '''notice:to make each append operation shorter, first we append the coordinates without offset.'''
            transformed_landmarks_dict_list.append({'center_x':landmarks[33][0],
                                        'center_y':landmarks[33][1],
                                        'name':'subnasale'})
            transformed_landmarks_dict_list.append({'center_x':landmarks[39][0],
                                        'center_y':landmarks[39][1],
                                        'name':'right inner canthus'})
            transformed_landmarks_dict_list.append({'center_x':landmarks[42][0],
                                        'center_y':landmarks[42][1],
                                        'name':'left inner canthus'})
            transformed_landmarks_dict_list.append({'center_x':landmarks[62][0],
                                        'center_y':landmarks[62][1],
                                        'name':'inferior upper lip border'})
            transformed_landmarks_dict_list.append({'center_x':landmarks[66][0],
                                        'center_y':landmarks[66][1],
                                        'name':'superior lower lip border'})
            transformed_landmarks_dict_list.append({'center_x':landmarks[36][0],
                                        'center_y':landmarks[36][1],
                                        'name':'right outer canthus'})
            transformed_landmarks_dict_list.append({'center_x':landmarks[45][0],
                                        'center_y':landmarks[45][1],
                                        'name':'left outer canthus'})
            transformed_landmarks_dict_list.append({'center_x':landmarks[48][0],
                                        'center_y':landmarks[48][1],
                                        'name':'right outer smile commissure'})
            transformed_landmarks_dict_list.append({'center_x':landmarks[54][0],
                                        'center_y':landmarks[54][1],
                                        'name':'left outer smile commissure'})
            transformed_landmarks_dict_list.append({'center_x':(landmarks[21][0]+landmarks[22][0])/2,
                                        'center_y':(landmarks[21][1]+landmarks[22][1])/2,
                                        'name':'soft tissue nasion'})
            transformed_landmarks_dict_list.append({'center_x':landmarks[8][0],
                                        'center_y':landmarks[8][1],
                                        'name':'soft tissue pogonion'})
            if self.display_tooth_landmarks==True:
                incisor_edge_x=landmarks[62][0]+self.incisor_edge_index*(landmarks[66][0]-landmarks[62][0])  #calculate the incisor edge point's x from the lip border distance.
                incisor_edge_y=landmarks[62][1]+self.incisor_edge_index*(landmarks[66][1]-landmarks[62][1])  #calculate the incisor edge point's y from the lip border distance.
                transformed_landmarks_dict_list.append({'center_x':incisor_edge_x,
                                        'center_y':incisor_edge_y,
                                        'name':'incisor edge'})
                transformed_landmarks_dict_list.append({'center_x':self.cuspid_edge_index*(landmarks[64][0]-landmarks[66][0])+landmarks[66][0]+landmarks[62][0]+self.incisor_edge_index*(landmarks[66][0]-landmarks[62][0])-landmarks[66][0],
                                        'center_y':(landmarks[65][1]-landmarks[66][1])*self.cuspid_edge_index*(landmarks[64][0]-landmarks[66][0])/(landmarks[65][0]-landmarks[66][0])+landmarks[66][1]+landmarks[62][1]+self.incisor_edge_index*(landmarks[66][1]-landmarks[62][1])-landmarks[66][1],
                                        'name':'left upper cuspid tip'})
                transformed_landmarks_dict_list.append({'center_x':self.cuspid_edge_index*(landmarks[60][0]-landmarks[66][0])+landmarks[66][0]+landmarks[62][0]+self.incisor_edge_index*(landmarks[66][0]-landmarks[62][0])-landmarks[66][0],
                                        'center_y':(landmarks[67][1]-landmarks[66][1])*self.cuspid_edge_index*(landmarks[60][0]-landmarks[66][0])/(landmarks[67][0]-landmarks[66][0])+landmarks[66][1]+landmarks[62][1]+self.incisor_edge_index*(landmarks[66][1]-landmarks[62][1])-landmarks[66][1],
                                        'name':'right upper cuspid tip'})
                dis_from_incisor_to_lip=self.dis_of_vec((incisor_edge_x,incisor_edge_y),
                                                        self.dconv(landmarks[62]),
                                                        ((landmarks[21][0]+landmarks[22][0])/2,(landmarks[21][1]+landmarks[22][1])/2),
                                                        self.dconv(landmarks[33])) #the l1
                cer_of_incisor_x=incisor_edge_x-self.incisor_length/dis_from_incisor_to_lip*(incisor_edge_x-landmarks[62][0])
                cer_of_incisor_y=incisor_edge_y-self.incisor_length/dis_from_incisor_to_lip*(incisor_edge_y-landmarks[62][1])
                transformed_landmarks_dict_list.append({'center_x':cer_of_incisor_x,
                                        'center_y':cer_of_incisor_y,
                                        'name':'cervical part of incisor'})
                print(self.incisor_edge_index)
            #transformed_landmarks_dict.
            '''now we add the offset and calculate.'''
            for value in transformed_landmarks_dict_list:
                value['center_x']-=self.image.shape[1]/2
                value['center_y']-=self.image.shape[0]/2
                self.landmarks_render(value)
        
        self.refresh()
            
    
    def cord_from_name(self,name:str):
        return(self.ui.landmark_list[name].coordinates_dict["center_x"]+self.ui.landmark_list[name].pos().x(),self.ui.landmark_list[name].coordinates_dict["center_y"]+self.ui.landmark_list[name].pos().y())

    def refresh(self):  #calcualte smile characteristics from self.landmarks, which
                        # is a list that stores all the Xs and Ys of previously detected landmarks.
        landmarks=self.landmarks
        angles={'canthus and smile commissure divation':str(self.angle_between_four_points(self.cord_from_name("right outer canthus")
                                                                            ,self.cord_from_name("left outer canthus")
                                                                            ,self.cord_from_name("right outer smile commissure")
                                                                            ,self.cord_from_name("left outer smile commissure"))),
                    'intercommissure width':str(self.dis_of_vec(self.cord_from_name("right outer smile commissure"),
                                                                                        self.cord_from_name("left outer smile commissure"),
                                                                                        self.cord_from_name("right inner canthus"),
                                                                                        self.cord_from_name("left inner canthus")
                                                                                        )),
                    'interlabial gap':str(self.dis_of_vec(self.cord_from_name("inferior upper lip border"),
                                                                                        self.cord_from_name("superior lower lip border"),
                                                                                        self.cord_from_name("soft tissue nasion"),
                                                                                        self.cord_from_name("subnasale")
                                                                                        )),
                    'philtrum height':str(self.dis_of_vec(self.cord_from_name("subnasale"),
                                                                                        self.cord_from_name("inferior upper lip border"),
                                                                                        self.cord_from_name("soft tissue nasion"),
                                                                                        self.cord_from_name("subnasale")
                                                                                        )),
                    'transverse symmetry':str(self.rel_dis(np.abs(self.ver_dis_from_point_to_vec(self.cord_from_name("left outer smile commissure"),
                                                                                    self.cord_from_name("soft tissue nasion"),
                                                                                    self.cord_from_name("soft tissue pogonion"))-
                                                    self.ver_dis_from_point_to_vec(self.cord_from_name("right outer smile commissure"),
                                                                                    self.cord_from_name("soft tissue nasion"),
                                                                                    self.cord_from_name("soft tissue pogonion"))),
                                                                                    self.cord_from_name("soft tissue nasion"),
                                                                                    self.cord_from_name("subnasale"))),
                    'vertical symmetry':str(self.angle_between_four_points(self.cord_from_name("left outer smile commissure")
                                                                            ,self.cord_from_name("right outer smile commissure")
                                                                            ,self.cord_from_name("soft tissue nasion")
                                                                            ,self.cord_from_name("soft tissue pogonion")))
                                                                                        }
        if self.display_tooth_landmarks==True:
            angles['upper dental angulation']=str(self.angle_between_four_points(self.cord_from_name("inferior upper lip border"),
                                                                                        self.cord_from_name("incisor edge"),
                                                                                        self.cord_from_name("soft tissue nasion"),
                                                                                        self.cord_from_name("subnasale")))
            angles['gingival display']=str(self.dis_of_vec(self.cord_from_name("inferior upper lip border"),
                                                                                        self.cord_from_name("cervical part of incisor"),
                                                                                        self.cord_from_name("soft tissue nasion"),
                                                                                        self.cord_from_name("subnasale")
                                                                                        ))
                                                                                        
        display=''
        for key,value in angles.items():
            display+=key+': '+value+'\n'
        self.ui.textEdit_2.setPlainText(display)

    def dconv(self,a)->(float,float): #dlib xy converter
        return a[0],a[1]
    
    def mol_of_vec(self,a:(float,float),b:(float,float))->float:
        vec=np.array((b[0]-a[0],b[1]-a[1]))
        mol_vec=np.sqrt(vec.dot(vec))
        return mol_vec
    
    def dis_of_vec(self,a:(float,float),b:(float,float),ref_a:(float,float),ref_b:(float,float))->float:
        mol_vec1=self.mol_of_vec(a,b)
        mol_vec_ref=self.mol_of_vec(ref_a,ref_b)
        return mol_vec1*self.conversion_factor/mol_vec_ref
    
    def ver_dis_from_point_to_vec(self,a:(float,float),b:(float,float),c:(float,float))->float: #c is the point.
        A=(b[1]-a[1])/(a[0]-b[0])
        B=1
        C=(b[1]-a[1])/(b[0]-a[0])*a[0]-a[1]
        distance=np.abs(A*c[0]+B*c[1]+C)/np.sqrt(A*A+B*B)
        return distance
    
    def rel_dis(self,distance:float,ref_a:(float,float),ref_b:(float,float))->float:
        mol_vec_ref=self.mol_of_vec(ref_a,ref_b)
        return distance*self.conversion_factor/mol_vec_ref

    def angle_between_four_points(self,a:(float,float),b:(float,float),c:(float,float),d:(float,float))->float:
        vec_1=np.array((b[0]-a[0],b[1]-a[1]))
        vec_2=np.array((d[0]-c[0],d[1]-c[1]))

        mol_vec_1=np.sqrt(vec_1.dot(vec_1))
        mol_vec_2=np.sqrt(vec_2.dot(vec_2))
        dot_product=vec_1.dot(vec_2)
        cos_=dot_product/(mol_vec_1*mol_vec_2)
        arccos_=np.arccos(cos_)
        return arccos_*180/np.pi #angle


    def landmarks_render(self,dict_for_landmarks): 
        '''dict for landmarks is a dict that stores the parameters to be passed to MyItem object.
        the structure of the dict is:{"center_x":int,"center_y":int,"name":str}
        ''' 
        self.ui.landmark_list[dict_for_landmarks['name']]=MyItem(dict_for_landmarks,self.ui.landmark_size) #allocate like this to ensure in the middle. -25 and -25 are the upper and left most of the coordinates.
        #self.ui.landmark_list[0].setPos(QtCore.QPointF(100,100))
        #self.ui.landmark_list[0].setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.ui.landmark_list[dict_for_landmarks['name']].inner_signal.mysignal.connect(self.refresh)
        self.ui.scene.addItem(self.ui.landmark_list[dict_for_landmarks['name']])
        print(self.ui.landmark_list[dict_for_landmarks['name']].transformOriginPoint().x())

        
        #self.ui.graphicsView.scene().setSceneRect(-200, -200, 400, 400) #very important for the whole accuracy!!!#allocate like this to ensure in the middle. -25 and -25 are the upper and left most of the coordinates.
        '''print(self.ui.landmark_list[0].)
        self.ui.graphicsView.setScene(self.ui.scene)'''

    def readcsv(self):
        #self.ui.pushButton_readcsv.setText("change_csv")
        read_dialog=read_Dialog(self) #parent window:mainwindow
        read_dialog.csv_source="xxx"
        read_dialog.ui.buttonBox.accepted.connect(lambda:self.csv_loader(read_dialog.csv_source)) #the lambda function is necessary for taking arguments.
        read_dialog.show()

    def csv_loader(self,csv_file):
        with open(csv_file) as file:
            loader=csv.DictReader(file)
            for lines in loader:
                self.landmarks_render({'center_x':float(lines['center_x']),'center_y':float(lines['center_y']),'name':lines['name']}) #pass the lines into the landmarks_render function and renders the landmarks to qlabel.
                print(lines)
            print(csv_file)
        pass
        
    def writecsv(self):
        #self.ui.pushButton_writecsv.setText("writing_csv")
        write_dialog=write_Dialog(self) #allocate self as the parent window.
        write_dialog.csv_source="xxx"
        self.identity="AI"
        write_dialog.mysignal.connect(self.process_sig_img)
        write_dialog.identity_signal.connect(self.rec_character)
        write_dialog.ui.buttonBox.accepted.connect(lambda:self.csv_exporter(write_dialog.csv_source)) #the lambda function is necessary for taking arguments.
        write_dialog.show()
    
    def process_sig_img(self,text):
        if text=='true':
            self.save_img=True
        else:
            self.save_img=False

    def rec_character(self,text):
        if text=="AI":
            self.identity="AI"
        elif text=="tester1":
            self.identity="tester1"
        elif text=="tester2":
            self.identity="tester2"

    def csv_exporter(self,csv_folder):
        content=[i.get_dict()for i in list(self.ui.landmark_list.values())]
        content_new=[{'center_x':str(x['center_x']),'center_y':str(x['center_y']),'name':x['name']} for x in content]

        if os.path.splitext(self.media_source)[-1]=='.jpg':
            csv_file=csv_folder+'/'+os.path.basename(self.media_source)+'.csv'
        if os.path.splitext(self.media_source)[-1]=='.mp4':
            csv_file=csv_folder+'/'+os.path.basename(self.media_source)+'-'+str(float((self.current_frame-1)/self.fps))+'.csv'

            if self.save_img==True:
                try:
                    cv2.imwrite(csv_folder+'/'+os.path.basename(self.media_source)+'-'+str(float((self.current_frame-1)/self.fps))+'.png',self.image)
                finally:pass
                #except:pass
        
        new_dict={}
        
        new_dict['filename']=csv_file

        if is_item_in_json("record.json",csv_file)==False:
            new_dict["content_AI"]=[{'center_x':'1','center_y':'1','name':x['name']} for x in content]
            new_dict["content_tester1"]=[{'center_x':'1','center_y':'1','name':x['name']} for x in content]
            new_dict["content_tester2"]=[{'center_x':'1','center_y':'1','name':x['name']} for x in content]
            if self.identity=="AI":
                new_dict["content_AI"]=content_new
            elif self.identity=="tester1":
                new_dict["content_tester1"]=content_new
            elif self.identity=="tester2":
                new_dict["content_tester2"]=content_new
            append_tojson("record.json",new_dict)
        
        else:
            with open("record.json",'r+') as file:
            # First we load existing data into a dict.
                file_data = json.load(file)

                for thing in file_data["emp_details"]:
                    try:
                        if thing['filename']==csv_file:
                            if self.identity=="AI":
                                thing["content_AI"]=content_new
                            elif self.identity=="tester1":
                                thing["content_tester1"]=content_new
                            elif self.identity=="tester2":
                                thing["content_tester2"]=content_new
                    except:
                        print('error detected')
                        pass
                file.seek(0)

                json.dump(file_data, file, indent = 4)

        fields=['center_x','center_y','name']
        try:
            file=open(csv_file,'w')
        except PermissionError:
            print("premission error")
            return
        with file:
            writer=csv.DictWriter(file,fieldnames= fields)
            writer.writeheader()

            print(content)

            print(content_new)

            writer.writerows(content)

    def is_ip_exist(self,ip_address):
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False
        
    def time_changed(self):
        print(self.total_frame)
        print(self.fps)
        print(self.ui.slider_time.value())
        frame_target=int(self.ui.slider_time.value()/10000*self.total_frame)

        self.current_frame=frame_target

        if self.vid.isOpened():
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_target)
        
        self.slider_allow_auto_move=True

        self.ui.time_setter.setText(str(float(self.current_frame/self.fps)))

        QtWidgets.QToolTip.showText(QtCore.QPoint(100,100), str(float(frame_target/self.fps)), self.ui.slider_time)
        print('time')

        img, self.image = self.vid.read()

        self.image  = imutils.resize(self.image ,height = 618 )

        if not self.image is None:
            self.update()

    def overcome_zig(self): #overcoming zigzags when toggling slide bar.
        self.slider_allow_auto_move=False

    def open_settings(self):
        set_dialog=set_Dialog(self)
        set_dialog.mysignal.connect(self.load_the_tooth)

        set_dialog.incisor_edge_index=self.incisor_edge_index

        set_dialog.cuspid_edge_index=self.cuspid_edge_index

        set_dialog.ui.lineEdit.setText(str(self.conversion_factor))

        set_dialog.ui.lineEdit_2.setText(str(self.incisor_length))

        if self.display_tooth_landmarks==True:
            set_dialog.ui.checkBox.setCheckState(1)
        else:
            set_dialog.ui.checkBox.setCheckState(0)
        if self.save_img==True:
            set_dialog.ui.checkBox_2.setCheckState(1)
        else:
            set_dialog.ui.checkBox_2.setCheckState(0)
        set_dialog.mysignal2.connect(self.save_the_image)
        set_dialog.mysignal3.connect(self.change_conversion_factor)
        set_dialog.mysignal5.connect(self.get_incisor_edge_index)
        set_dialog.mysignal6.connect(self.get_cuspid_edge_index)
        set_dialog.mysignal7.connect(self.get_incisor_length)

        set_dialog.show()

    def load_the_tooth(self,text):
        if text=='true':
            self.display_tooth_landmarks=True
        else:
            self.display_tooth_landmarks=False 

    def save_the_image(self,text):
        if text=='true':
            self.save_img=True
        else:
            self.save_img=False 

    def get_incisor_edge_index(self,text):
        try:
            self.incisor_edge_index=float(text)
            incisor_edge_x=int(self.landmarks[62][0]+self.incisor_edge_index*(self.landmarks[66][0]-self.landmarks[62][0])-self.image.shape[1]/2)  #calculate the incisor edge point's x from the lip border distance.
            incisor_edge_y=int(self.landmarks[62][1]+self.incisor_edge_index*(self.landmarks[66][1]-self.landmarks[62][1])-self.image.shape[0]/2)  #calculate the incisor edge point's y from the lip border distance.

            incisor_point={'center_x':incisor_edge_x,
                            'center_y':incisor_edge_y,
                            'name':'incisor edge'}
            
            if 'incisor edge' in self.ui.landmark_list:  #search the landmark_list
                self.ui.landmark_list['incisor edge'].set_position(incisor_point['center_x'],incisor_point['center_y'])
            else:
                self.ui.landmark_list['incisor edge']=MyItem(incisor_point,self.ui.landmark_size)
                self.ui.landmark_list['incisor edge'].inner_signal.mysignal.connect(self.refresh)  #接通refresh
                self.ui.scene.addItem(self.ui.landmark_list['incisor edge'])
                print('added!!!!!!!!!!!!!!!!!!!!!!!"')
                print(incisor_edge_x,incisor_edge_y)
        except:
            print('incisor error')
        finally:
            pass

    def get_cuspid_edge_index(self,text):
        try:
            self.cuspid_edge_index=float(text)
        finally:
            pass

    def get_incisor_length(self,text):
        try:
            self.incisor_length=float(text)
        finally:
            pass

    def change_conversion_factor(self,text):
        try:
            self.conversion_factor=float(text)
            self.refresh()
        except AttributeError:
            print("please load landmrks first.")
        finally:
            pass



if __name__ == '__main__':
    app = QApplication(sys.argv) # 创建app，用 QApplication 类
    cutomUI = CustomUI()
    cutomUI.show()
    sys.exit(app.exec_())

'''
12.10 task: write_csv dialog choose different image.
'''
'''
to do: add dlib reconizing function.
'''
'''
to do: add scroll bar.
'''