'''
*******************************
*
*                ===============================================
*                   Nirikshak Bot (NB) Theme (eYRC 2020-21)
*                ===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*******************************
'''

# Team ID:            [ Team-ID ]
# Author List:        [ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:            task_1b.py
# Functions:        applyPerspectiveTransform, detectMaze, writeToCsv
#                     [ Comma separated list of functions in this file ]
# Global variables:
#                     [ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

def orderpoints(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    dif = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(dif)]
    rect[3] = pts[np.argmax(dif)]
    return rect


def four_point_transform(image, pts):
    rect = orderpoints(pts)
    (tl, tr, br, bl) = rect
    maxWidth = 512
    maxHeight = 512
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def fun(im):
    val = 0

    gate = [False, False, False, False]
    for i in range(0, 5, 1):
        if not gate[0] and im[i, 50] == 0:
            val = val + 2
            gate[0] = True
        if not gate[1] and im[99-i, 50] == 0:
            val = val + 8
            gate[1] = True
        if not gate[2] and im[50, i] == 0:
            val = val + 1
            gate[2] = True
        if not gate[3] and im[50, 99-i] == 0:
            val = val + 4
            gate[3] = True

    return val


'''def applyPerspectiveTransform(client_id,input_img):
    warped_img = None
    img = input_img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 75, 200)
    _, thresh = cv2.threshold(edged, 127, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    screenCnt = None
    flag = False
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            flag = True
            break
        elif len(approx) != 4:
            cv2.drawContours(img, cnts, -1, (0, 255, 0), 2)
            cv2.imshow("Outline", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
    warped_img = four_point_transform(img, screenCnt.reshape(4, 2))
    warped_img = cv2.resize(warped_img, (1280, 1280))
    cv2.imshow("Outline", warped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return warped_img'''
def applyPerspectiveTransform(client_id,input_img):
    """
    Purpose:
    ---
    takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

    Input Arguments:
    ---
    `input_img` :   [ numpy array ]
        maze image in the form of a numpy array

    Returns:
    ---
    `warped_img` :  [ numpy array ]
        resultant warped maze image after applying Perspective Transform

    Example call:
    ---
    warped_img = applyPerspectiveTransform(input_img)
    """

    warped_img = None
    x=0
    img = input_img
    '''cv2.imshow('input',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    '''cv2.imshow('gray',gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    blur = cv2.GaussianBlur(img,(5,5),0)
    edged = cv2.Canny(blur, 75, 200)
    _, thresh = cv2.threshold(edged, 127, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, cnts, -1, [0,255,255],3)
    '''cv2.imshow('cnt',thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break
    warped = four_point_transform(img, screenCnt.reshape(4, 2))
    padded = cv2.copyMakeBorder(warped, 1, 1, 1, 1, cv2.BORDER_CONSTANT)
    warped_img = cv2.resize(padded, (1280, 1280))
    ##################################################

    return warped_img

def applyPerspectiveTransform_vs(client_id,input_img):
    warped_img = None
    img = input_img
    min_x=1000000
    min_y=1000000
    max_x=-1
    max_y=-1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 75, 200)
    _, thresh = cv2.threshold(edged, 127, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        #print(approx)
        for pt in approx :
            min_x = min(min_x,pt[0][0])
            min_y = min(min_y,pt[0][1])
            max_x = max(max_x,pt[0][0])
            max_y = max(max_y,pt[0][1])
    print(min_x,max_x,min_y,max_y)
    screenCnt=np.array([[min_x,min_y],[min_x,max_y],[max_x,max_y],[max_x,min_y]])
    print(screenCnt)
        
    warped = four_point_transform(img, screenCnt)
    padded = cv2.copyMakeBorder(warped, 1, 1, 1, 1, cv2.BORDER_CONSTANT)
    warped_img = cv2.resize(padded, (1280, 1280))
    cv2.imshow("Outline", warped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return warped_img


def detectMaze(warped_img):
    """
    Purpose:
    ---
    takes the warped maze image as input and returns the maze encoded in form of a 2D array

    Input Arguments:
    ---
    `warped_img` :    [ numpy array ]
        resultant warped maze image after applying Perspective Transform

    Returns:
    ---
    `maze_array` :    [ nested list of lists ]
        encoded maze in the form of a 2D array

    Example call:
    ---
    maze_array = detectMaze(warped_img)
    """

    ##############    ADD YOUR CODE HERE    ##############
    img = warped_img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, (1000, 1000))
    l = []
    for x in range(0, 1000, 100):
        l2 = []
        for y in range(0, 1000, 100):
            im = img[x:x + 100, y:y + 100]
            val = fun(im)
            l2.append(val)
        l.append(l2)

    maze_array = l
    ##################################################

    return maze_array


# NOTE:    YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):
    """
    Purpose:
    ---
    takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

    Input Arguments:
    ---
    `csv_file_path` :    [ str ]
        file path with name for csv file to write

    `maze_array` :        [ nested list of lists ]
        encoded maze in the form of a 2D array

    Example call:
    ---
    warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
    """

    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(maze_array)


# NOTE:    YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
#                     as input, applies Perspective Transform by calling applyPerspectiveTransform function,
#                     encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
#                     by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
#                     present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
#                     applyPerspectiveTransform and detectMaze functions.

if __name__ == "_main_":

    # path directory of images in 'test_cases' folder
    img_dir_path = 'test_cases/'

    # path to 'maze00.jpg' image file
    file_num = 0
    img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

    print('\n============================================')
    print('\nFor maze0' + str(file_num) + '.jpg')

    # path for 'maze00.csv' output file
    csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

    # read the 'maze00.jpg' image file
    input_img = cv2.imread(img_file_path)

    # get the resultant warped maze image after applying Perspective Transform
    warped_img = applyPerspectiveTransform(input_img)

    if type(warped_img) is np.ndarray:

        # get the encoded maze in the form of a 2D array
        maze_array = detectMaze(warped_img)

        if (type(maze_array) is list) and (len(maze_array) == 10):

            print('\nEncoded Maze Array = %s' % (maze_array))
            print('\n============================================')

            # writes the encoded maze array to the csv file
            writeToCsv(csv_file_path, maze_array)

            cv2.imshow('warped_img_0' + str(file_num), warped_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:

            print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
            exit()

    else:

        print(
            '\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
        exit()

    choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

    if choice == 'y':

        for file_num in range(1, 10):

            # path to image file
            img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

            print('\n============================================')
            print('\nFor maze0' + str(file_num) + '.jpg')

            # path for csv output file
            csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

            # read the image file
            input_img = cv2.imread(img_file_path)

            # get the resultant warped maze image after applying Perspective Transform
            warped_img = applyPerspectiveTransform(input_img)

            if type(warped_img) is np.ndarray:

                # get the encoded maze in the form of a 2D array
                maze_array = detectMaze(warped_img)

                if (type(maze_array) is list) and (len(maze_array) == 10):

                    print('\nEncoded Maze Array = %s' % (maze_array))
                    print('\n============================================')

                    # writes the encoded maze array to the csv file
                    writeToCsv(csv_file_path, maze_array)

                    cv2.imshow('warped_img_0' + str(file_num), warped_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                else:

                    print(
                        '\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
                    exit()

            else:

                print(
                    '\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
                exit()

    else:

        print('')