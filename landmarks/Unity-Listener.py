# Imports and Constants
# Python 2.7

import cv2
import dlib
import numpy as np
import time
import sys
from operator import add
import socket

## Our pretrained model that predicts the rectangles that correspond to the facial features of a face
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
CASCADE_PATH='Haarcascades/haarcascade_frontalface_default.xml'

FACE_POINTS = list(range(17, 68))
MOUTH_POINTS = list(range(48, 61))
RIGHT_BROW_POINTS = list(range(17, 22))
LEFT_BROW_POINTS = list(range(22, 27))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
NOSE_POINTS = list(range(27, 35))
JAW_POINTS = list(range(0, 17))
AVG = None

# Points used to line up the images.
ALIGN_POINTS = (LEFT_BROW_POINTS + RIGHT_EYE_POINTS + LEFT_EYE_POINTS +
                               RIGHT_BROW_POINTS + NOSE_POINTS + MOUTH_POINTS)

# Points from the second image to overlay on the first. The convex hull of each
# element will be overlaid.
OVERLAY_POINTS = [
    LEFT_EYE_POINTS + RIGHT_EYE_POINTS + LEFT_BROW_POINTS + RIGHT_BROW_POINTS,
    NOSE_POINTS + MOUTH_POINTS,
]


# 3D model points.
POSE_PTS = (30, 8, 36, 45, 48, 54)
model_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -330.0, -65.0),        # Chin
                            (-225.0, 170.0, -135.0),     # Left eye left corner
                            (225.0, 170.0, -135.0),      # Right eye right corne
                            (-150.0, -150.0, -125.0),    # Left Mouth corner
                            (150.0, -150.0, -125.0)      # Right mouth corner
                        
                        ])

# bounding box
CASCADE = cv2.CascadeClassifier(CASCADE_PATH)
DETECTOR = dlib.get_frontal_face_detector()

# facial landmarks
PREDICTOR = dlib.shape_predictor(PREDICTOR_PATH)


# Live Landmark Functions

def get_landmarks(im, dlibOn, const_rect=None, show_rect=False):
    if const_rect == None:
        pass
    else:
        s = const_rect  # (79, 51) (208, 180)
        if show_rect:
            draw_rect(im, s)
        rect = dlib.rectangle(s[0][0], s[0][1], s[1][0], s[1][1])
        a = np.matrix([[p.x, p.y] for p in PREDICTOR(im, rect).parts()])
        
        if a is None:
            print("no a")
            return None
        
        return a
    
    if dlibOn:
        rects = DETECTOR(im, 1)
        if len(rects) < 1:
            print("no faces")
            return None

        if show_rect:
            draw_rect(im, dlib_rect_to_tuple(rects[0]))
            #print(rects[0].left())
        a = np.matrix([[p.x, p.y] for p in PREDICTOR(im, rects[0]).parts()])
        return a
    
    else:
        rects = CASCADE.detectMultiScale(im, 1.3, 5, flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) < 1:
            print("no faces")
            return None
        
        x,y,w,h = rects[0]
        
        x = long(x)
        y = long(y)
        rect=dlib.rectangle(x,y,x+w,y+h)
        if show_rect:
            draw_rect(im, rect)
        return np.matrix([[p.x, p.y] for p in PREDICTOR(im, rect).parts()])

    
def annotate_landmarks(im, landmarks):
    im = im.copy()
    for idx, point in enumerate(landmarks):
        pos = (point[0, 0], point[0, 1])
        #cv2.putText(im, str(idx), pos,
        #            fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        #            fontScale=0.4,
        #            color=(0, 0, 255))
        cv2.circle(im, pos, 3, color=(0, 255, 255))
    return im


def face_swap(img, name, cr=None):

    s = get_landmarks(img,True, const_rect=cr)
    
    if not s:
        print "No or too many faces"
        return img
    
    img = annotate_landmarks(img, s)
    img = draw_rect(img, s[0])
    
    #frame = cv2.resize(image,None,fx=4, fy=4, interpolation = cv2.INTER_LINEAR)
    
    return image 


# draw rectangle (79, 51) (208, 180)
def draw_rect(img, s):
    if not s:
        return img

    a = s[0]
    b = s[1]
    cv2.line(frame, a,           (a[0],b[1]), (255,0,0))
    cv2.line(frame, (a[0],b[1]), b,           (255,0,0))
    cv2.line(frame, b,           (b[0],a[1]), (255,0,0))
    cv2.line(frame, (b[0],a[1]), a,           (255,0,0))
    
    return img


def open_camera(num=0):
    cap = cv2.VideoCapture(num)
    if cap.isOpened():
        #print("got cam")
        return cap
    else:
        print("no cam")
        cap.release()
        return None

    
def dlib_rect_to_tuple(rect):
    return [(rect.left(), rect.top()), (rect.right(), rect.bottom())]


def get_relevant_pts(landmarks):
    a = []
    for i in range(len(POSE_PTS)):
        a.append( (landmarks[POSE_PTS[i],0], landmarks[POSE_PTS[i],1]) )
    return np.array(a, dtype='double')


def put_pose(im, image_points):
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points,\
                                                                  camera_matrix, dist_coeffs, flags=cv2.CV_ITERATIVE)

    #print "Rotation Vector:\n {0}".format(rotation_vector)
    #print "Translation Vector:\n {0}".format(translation_vector)
    

    # Project a 3D point (0, 0, 500.0) onto the image plane.
    # We use this to draw a line sticking out of the nose
    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 500.0)]), rotation_vector,\
                                                 translation_vector, camera_matrix, dist_coeffs)

    for p in image_points:
        cv2.circle(im, (int(p[0]), int(p[1])), 3, (0,0,255), -1)


    p1 = ( int(image_points[0][0]), int(image_points[0][1]))
    p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

    cv2.line(im, p1, p2, (255,0,0), 2)
    
    return (rotation_vector, translation_vector)
    

TIME = None
F_COUNT = 0
F_RATE = 0
def put_frame_rate_and_vectors(im, vectors=None):
    global TIME
    global F_COUNT
    global F_RATE
    
    pos = (10,30)
    t = time.clock()

    diff = t - TIME
    F_COUNT += 1
    
    if diff > 1:
        TIME = t
        F_RATE = F_COUNT
        F_COUNT = 0
        
    cv2.putText(im, str(F_RATE),
                pos,
                fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                fontScale=0.4,
                thickness=2,
                color=(0, 0, 255))
    
    if vectors:
        cv2.putText(im, "R: ({:+f},{:+f},{:+f})".format(vectors[0][0,0]*(180/3.14), vectors[0][1,0]*(180/3.14), vectors[0][2,0]*(180/3.14)),
        #cv2.putText(im, "R: ({:+f})".format(vectors[0][0,0]),
                (pos[0], pos[1]+20),
                fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                fontScale=0.6,
                thickness=2,
                color=(0, 0, 255))
        cv2.putText(im, "T: ({:+f},{:+f},{:+f})".format(vectors[1][0,0], vectors[1][1,0], vectors[1][2,0]),
                (pos[0], pos[1]+40),
                fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                fontScale=0.6,
                thickness=2,
                color=(0, 0, 255))
    else:
        cv2.putText(im, "---",
                (pos[0], pos[1]+20),
                fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                fontScale=0.4,
                color=(0, 0, 255))
        
    
    return im


def setup_socket(host="localhost", port="10000"):

    HOST = host
    PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind( (HOST,PORT) )
    print("listening...")
    sock.listen(1)

    conn, addr = sock.accept()
    print("Connected: ", addr)
    #while 1:
    #    data = conn.recv(1024)
    #    print("",data)
    #    if data.strip() == "":
    #        break
    #    conn.sendall(data) #mirrors
    #
    #conn.close()

    #print("Connection Closed.")

    return conn


# TODO: avg x by adding and subtracting (curr and oldest)
#    -last --- moving-avg --- +new
LANDMARKS = None
def avg_landmarks(curr, past):
    global LANDMARKS
    if past != None:
        landmarks = np.add(curr, past)
    landmarks //= 2
    prev_landmarks = landmarks
    
    

def return_points(landmarks):
    # 36L, 45R
    return ( (landmarks[36,0],landmarks[36,1]), (landmarks[45,0],landmarks[45,1]) )
    
    
    
# Main ##################################

# Name is the image we want to swap onto ours
# dlibOn controls if use dlib's facial landmark detector (better) 
# or use HAAR Cascade Classifiers (faster)
cap = open_camera(0)
if not cap:
    sys.exit()
    
ret, frame = cap.read()
size = frame.shape
    
# Camera internals
focal_length = size[1]
center = (size[1]/2, size[0]/2)
camera_matrix = np.array(
                         [[focal_length, 0, center[0]],
                         [0, focal_length, center[1]],
                         [0, 0, 1]], dtype = "double"
                        )
print "Camera Matrix :\n {0}".format(camera_matrix);
print "Camera Size: \n{0}".format(size);
dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion

dlibOn = False
counter = 0
landmarks = None
prev_landmarks = None
TIME = time.clock()

HOST = "localhost"
PORT = 10000
SOCK = setup_socket(HOST, PORT)

while True:
    counter += 1

    ret, frame = cap.read()
    
    #Reduce image size by 50% to reduce processing time and improve framerates
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    
    # flip image so that it's more mirror like
    frame = cv2.flip(frame, 1)
    
    #face_box = [(179,151), (456,440)]
    face_box = None
    
    # No processing
    #cv2.imshow('window_name', frame)
    #if cv2.waitKey(1) == 13: #13 is the Enter Key
    #    break
    #continue
    
    landmarks = get_landmarks(frame, True, const_rect=face_box, show_rect=True)
    
    if landmarks != None and counter > 1: #average 2 frames, less jitter
        if prev_landmarks != None:
            landmarks = np.add(landmarks, prev_landmarks)
        landmarks //= 2
        prev_landmarks = landmarks
        # TODO: avg x by adding and subtracting (curr and oldest)
        
    if landmarks != None:  # annotating landmarks, adding lines
        frame = annotate_landmarks(frame, landmarks)
        cv2.line(frame, (landmarks[36,0],landmarks[36,1]), (landmarks[45,0],landmarks[45,1]), (255,0,0))
        #print((landmarks[36,0],landmarks[36,1]), (landmarks[45,0],landmarks[45,1]))
        
    vectors = None
    if landmarks != None:  # adds pose estimation
        a = get_relevant_pts(landmarks)
        vectors = put_pose(frame, a)
    
    # resize, then add vectors
    frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    frame = put_frame_rate_and_vectors(frame, vectors=vectors)
    
    # Send points
    data = SOCK.recv(1024)

    # TODO: points right now are sides of eyes (average corners)
    if landmarks != None:
        pts = return_points(landmarks)
        SOCK.sendall( "(" + str(pts[0]) + ", " + str(pts[1]) + ", {:f}".format(vectors[0][2,0]) + ")\n" )
    else: SOCK.sendall("((1000, 1000), (1100, 1100), 0)\n")

    #conn.close()
    #print("Connection Closed.")
    
    # Show image
    
    cv2.imshow('window_name', frame)
    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break

cap.release()
cv2.destroyAllWindows()
