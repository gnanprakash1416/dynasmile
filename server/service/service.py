from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
from library.bucket_test import download_func
from library.test_batch_detections import load_model, detect_face, face_cord
import boto3
import numpy as np
from deepface import DeepFace
import cv2
import os
import imutils
import logging
from sixdrepnet import SixDRepNet
from math import sqrt, cos
import math

os.environ['DEEPFACE_LOG_LEVEL'] = str(logging.ERROR)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '1'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
s3_client = boto3.client('s3')

detector = load_model()  # the MTCNN face recognition model
detector.eval()  # important

model_repnet = SixDRepNet()

current_frame = 0
video_analyzing = False

'''This is the part for iniitializing model.'''
model_ori = DeepFace.build_model("Emotion")
emotion_labels_ori = [
    'angry',
    'disgust',
    'fear',
    'happy',
    'sad',
    'surprise',
    'neutral']
face_cascade_ori = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml')


def mol_of_vec(a: (float, float), b: (float, float)) -> float:
    vec = np.array((b[0] - a[0], b[1] - a[1]))
    mol_vec = np.sqrt(vec.dot(vec))
    return mol_vec


def emotion_detector(image, face_cascade, model):
    '''The  detection of blank frame is necessary.'''
    try:
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except BaseException:
        return 0, 0, 0
    faces = face_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(
            30,
            30))

    '''This is used to ensure there's only one face in the frame.'''
    if len(faces) > 1:
        x1, x2, y1, y2 = face_cord(detector, image)
        face_roi = gray_frame[y1:y2, x1:x2]
        # Resize the face ROI to match the input shape of the model
        resized_face = cv2.resize(
            face_roi, (48, 48), interpolation=cv2.INTER_AREA)

        # Normalize the resized face image
        normalized_face = resized_face / 255.0

        # Reshape the image to match the input shape of the model
        reshaped_face = normalized_face.reshape(1, 48, 48, 1)

        # Predict emotions using the pre-trained model
        preds = model.predict(reshaped_face)[0]
        emotion_idx = preds.argmax()
        happiness_value = preds[3]
        print(happiness_value)
        return 10000, 10000, happiness_value
    if len(faces) < 1:
        # meaning the three are all None. Here we use -1,-1,-1 to represent the
        # sppecial face situation. Hwever, to make it compatible with other
        # functions, we have to do post-operations to convert them into zeros.
        return -1, -1, -1

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = gray_frame[y:y + h, x:x + w]

        # Resize the face ROI to match the input shape of the model
        resized_face = cv2.resize(
            face_roi, (48, 48), interpolation=cv2.INTER_AREA)

        # Normalize the resized face image
        normalized_face = resized_face / 255.0

        # Reshape the image to match the input shape of the model
        reshaped_face = normalized_face.reshape(1, 48, 48, 1)

        # Predict emotions using the pre-trained model
        preds = model.predict(reshaped_face)[0]
        emotion_idx = preds.argmax()
        happiness_value = preds[3]
        print(happiness_value)
        return emotion_idx, preds, happiness_value


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    print("emitted")


'''Now we are writing the s3 part. This part can listen the message from client,
then it will download image to do analyse.'''


@socketio.on('s3_retrieve')
# message is a dict object. It can be transmitted directly.
def download_and_analyze(message):
    print(message)
    global s3_client
    download_func(s3_client, message['filename'], 'frank--bucket', 'test/')
    emotion_idx, preds, happiness_value = emotion_detector(cv2.imread(
        'test/' + os.path.basename(message['filename'])), face_cascade_ori, model_ori)
    emit('image_evaluated', {'happiness value': str(happiness_value)})
    emit('send_list', json.dumps([1, 1, 1, 1]))


'''This function is used to download and analyze video from s3'''


@socketio.on('analyze_uploaded_video_and_generate_emotion_list')
def analyze_video(video):
    global current_frame, video_analyzing
    current_frame = 0
    video_analyzing = True
    print("video received: " + video['filename'])
    global s3_client
    # download the video to test folder.
    download_func(s3_client, video['filename'], 'frank--bucket', 'test/')
    vid = cv2.VideoCapture('./test/' + os.path.basename(video['filename']))
    print('./test/' + os.path.basename(video['filename']))
    print("miss" + str(vid.get(cv2.CAP_PROP_CHANNEL)))
    emotion_list = []
    commissure_list = []
    face_list = []
    face_not_detected = 0
    face_greater_than_one_cv2_only = 0
    face_greater_than_one_mobile = 0
    wrong_happiness_value = []
    nasion_list = []  # the list for the storage of mid faical high.
    leftx_eye_list = []
    lefty_eye_list = []
    while (vid.isOpened()):
        img, image = vid.read()
        emit('video_analyzing', str(current_frame))
        if image is None:
            break
        image = imutils.resize(image, height=618)
        emotion_idx, preds, happiness_value = emotion_detector(
            image, face_cascade_ori, model_ori)

        # Here is the filter to convert back to zeros.
        if emotion_idx == -1:
            face_not_detected += 1
            emotion_idx, preds, happiness_value = 0, 0, 0
        if emotion_idx == 10000:
            face_greater_than_one_cv2_only += 1
            wrong_happiness_value.append(preds)  # intentially

            # emotion_idx,preds,happiness_value=0,0,0
        # generate full emotion list that contains every frame.
        emotion_list.append(happiness_value)
        if happiness_value > 0.9:
            landmarks = detect_face(detector, image)

            pitch, yaw, roll = model_repnet.predict(image)

            if landmarks is not None:
                if landmarks == []:
                    commissure_list.append(0)
                    nasion_list.append(0)
                    leftx_eye_list.append(0)
                    lefty_eye_list.append(0)
                    face_greater_than_one_mobile += 1
                else:
                    commissure_list.append(
                        mol_of_vec(
                            (landmarks[48][0], landmarks[48][1]), (landmarks[54][0], landmarks[54][1])))
                    #
                    lefteye_x = 0
                    lefteye_y = 0
                    for i in range(36, 42):
                        lefteye_x += landmarks[i][0]
                        lefteye_y += landmarks[i][1]
                        # this *5 is for testing and zooming.
                        lefteye_x = lefteye_x / 6 * 2.5
                        lefteye_y = lefteye_y / 6 * 2.5
                        lefteye = [lefteye_x, lefteye_y]

                        righteye_x = 0
                        righteye_y = 0
                    for i in range(42, 48):
                        righteye_x += landmarks[i][0]
                        righteye_y += landmarks[i][1]
                        righteye_x = righteye_x / 6 * 2.5
                        righteye_y = righteye_y / 6 * 2.5
                        righteye = [righteye_x, righteye_y]
                    nasion_mol = mol_of_vec(
                        (lefteye[0], lefteye[1]), (righteye[0], righteye[1]))
                    nasion_list.append(sqrt(((nasion_mol / cos(pitch[0] / (180 / math.pi)))**2 + (
                        nasion_mol / cos(yaw[0] / (180 / math.pi)))**2) / 2))
                    leftx_eye_list.append(lefteye[0])
                    lefty_eye_list.append(lefteye[1])
            else:
                commissure_list.append(0)
                nasion_list.append(0)
                leftx_eye_list.append(0)
                lefty_eye_list.append(0)

        else:
            commissure_list.append(0)
            nasion_list.append(0)
            leftx_eye_list.append(0)
            lefty_eye_list.append(0)
        current_frame += 1

    vid.release()
    print('ddone')

    nasion__min = min([ii for ii in nasion_list if ii != 0])
    conversion_list = [float(nasion__min / xx) if xx !=
                       0 else 1 for xx in nasion_list]

    emit('emotion_list_of_video',
         json.dumps({'name': video['filename'],
                     'emotion_list': [float(ii) for ii in emotion_list],
                     'commissure_list': [float(ii) for ii in commissure_list],
                     'nasion_list': [float(ii) for ii in nasion_list],
                     'conversion_list': conversion_list,
                     'leftx_eye_list': leftx_eye_list,
                     'lefty_eye_list': lefty_eye_list,
                     'face_not_detected': face_not_detected,
                     'face_greater_than_one_cv2_only': face_greater_than_one_cv2_only,
                     'face_greater_than_one_mobile': face_greater_than_one_mobile}))

    data = {
        'name': video['filename'],
        'emotion_list': [
            float(ii) for ii in emotion_list],
        'commissure_list': [
            float(ii) for ii in commissure_list],
        'nasion_list': [
            float(ii) for ii in nasion_list],
        'conversion_list': conversion_list,
        'leftx_eye_list': leftx_eye_list,
        'lefty_eye_list': lefty_eye_list,
        'face_not_detected': face_not_detected,
        'face_greater_than_one_cv2_only': face_greater_than_one_cv2_only,
        'face_greater_than_one_mobile': face_greater_than_one_mobile}
    with open('result.json', 'w') as f:
        json.dump(data, f)
    video_analyzing = False


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('How s it going')
def handle_client_disconnection(message):
    global current_frame, video_analyzing
    try:
        if video_analyzing == True:
            emit('video_analyzing', str(current_frame))
        else:
            with open('result.json', 'r') as file:
                emit('emotion_list_of_video', json.dumps(json.load(file)))
                emit('video_analyzing', str(current_frame))
    except BaseException:
        pass


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False)
