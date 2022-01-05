import cv2
import os
import time

def get_frames(inputFile,outputFolder,step,count):

  #initializing local variables
  step = step
  frames_count = count

  currentframe = 0
  frames_captured = 0

  #creating a folder
  try:  
      # creating a folder named data 
      if not os.path.exists(outputFolder): 
          os.makedirs(outputFolder) 
    
  #if not created then raise error 
  except OSError: 
      print ('Error! Could not create a directory') 
  
  #reading the video from specified path 
  cam = cv2.VideoCapture(inputFile) 

  #reading the number of frames at that particular second
  frame_per_second = cam.get(cv2.CAP_PROP_FPS)

  while (True):
      ret, frame = cam.read()
      if ret:
          if currentframe > (step*frame_per_second):  
              currentframe = 0
              #saving the frames (screenshots)
              name = r"C:\Users\SMORONTA\Documents\Datasets_ultimate\imagenes_tomadas\overripe_pineapple\overripe_pineapple_" + str(frames_captured) + '.jpg'
              print ('Creating...' + name) 
              
              cv2.imwrite(name, frame)       
              frames_captured+=1
              
              #breaking the loop when count achieved
              if frames_captured > frames_count-1:
                ret = False
          currentframe += 1           
      if ret == False:
          break
  
  #Releasing all space and windows once done
  cam.release()
  cv2.destroyAllWindows()

input_file = r"C:\Users\SMORONTA\Pictures\Camera Roll\overripe_pineapple.mp4"
output_file = r"C:\Users\SMORONTA\Documents\Datasets_ultimate\imagenes_tomadas\overripe_pineapple"
count = 10000
step = 0.3
get_frames(input_file,output_file,step,count)