#generated from best cubic fit of three values i guessed, plus (0,0) obviously
cubicSensitivity=46
#quadraticSensitivity=100
linearSensitivity=4.8 #lower because cubics are multiples of [0..1]
sensitivity_exponent=1	#wut
normalizationTolerance=.02
invert=1   #1 for non-inversion -1 for inversion

import pygame
import win32api, win32con
from time import sleep
import math
pygame.init()


joystick_count=pygame.joystick.get_count()
if joystick_count == 0:
	# No joysticks!
	print ("Error, I didn't find any joysticks.")
else:
	index=0
	success_init_joystick=False
	while not success_init_joystick and index < joystick_count:
		try:
			my_joystick = pygame.joystick.Joystick(index)
			success_init_joystick=True
			index+=1
		except Exception:
			success_init_joystick=False
			
	#todo
	#print("multiple joysticks, please touch the one you want to use")

my_joystick.init()



#find the normalization values

normalCount=0
normalTimeout=0
normal=(0,0)
joystickSameCount=0
remainder=(0,0)
# while normalCount<10 and normalTimeout<400:
	# pygame.event.get()
	# cursor_pos=(my_joystick.get_axis(0),my_joystick.get_axis(1))
	# if normal!=cursor_pos[0] or y_normal!=cursor_pos[1]:
		# normal_count=0 #make sure we get 10 of the same in a row
	# normal[0]=cursor_pos[0]
	# normal[1]=cursor_pos[1]
	# normalCount+=1
	# normalTimeout+=1
	# sleep(.03)
	
#for logitech extreme 3d pro, the tick value is 0.00785 (ish) and doesnt normalize well
	
done=False
joyDiff=(0,0)
while done==False:
 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done=True
		elif event.type == pygame.JOYBUTTONUP and event.button == 0:
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
		elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
		elif event.type == pygame.JOYBUTTONUP and event.button == 1:
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0,0)
		elif event.type == pygame.JOYBUTTONDOWN and event.button == 1:
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0,0)
		elif event.type == pygame.JOYBUTTONUP and event.button == 2:
			win32api.mouse_event(0x0100,0,0,0x0001,0)
		elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:
			win32api.mouse_event(0x0080,0,0,0x0001,0)
		elif event.type == pygame.JOYBUTTONUP and event.button == 4:
			win32api.mouse_event(0x0100,0,0,0x0002,0)
		elif event.type == pygame.JOYBUTTONDOWN and event.button == 4:
			win32api.mouse_event(0x0080,0,0,0x0002,0)
		elif event.type == pygame.JOYBUTTONUP and event.button == 3:
			win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,0,0,0,0)
		elif event.type == pygame.JOYBUTTONDOWN and event.button == 3:
			win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,0,0,0,0)
			
		
	# As long as there is a joystick
	if joystick_count != 0:
	 
		# This gets the position of the axis on the game controller
		# It returns a number between -1.0 and +1.0
		
		
		newJoyDiff = (my_joystick.get_axis(0),my_joystick.get_axis(1))
		if joyDiff[0]==newJoyDiff[0] and joyDiff[1] == newJoyDiff[1] and math.fabs(newJoyDiff[0])<normalizationTolerance and math.fabs(newJoyDiff[1])<normalizationTolerance:
			joystickSameCount+=1
			if joystickSameCount>20:
				normal = joyDiff
				joystickSameCount=0
				print "renormalized!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		else:
			joystickSameCount=0
		joyDiff=newJoyDiff
		joyNorm=(joyDiff[0]-normal[0],joyDiff[1]-normal[1])
		try:		
			cursorPos=win32api.GetCursorPos()
			
			distance2=(joyNorm[0]*joyNorm[0]+joyNorm[1]*joyNorm[1])
			#distance=(math.sqrt(distance2)) #not needed for cubic implementation from dot product calculation
			
		
			#cubic implementation
			mouseDiff=(joyNorm[0]*linearSensitivity+joyNorm[0]*distance2*cubicSensitivity,
				invert*(joyNorm[1]*linearSensitivity+joyNorm[1]*distance2*cubicSensitivity))
			
			

			
			win32api.SetCursorPos((int(cursorPos[0]+mouseDiff[0]+remainder[0]),int(cursorPos[1]+mouseDiff[1]+remainder[1])))
			win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE,int(cursorPos[0]+mouseDiff[0]+remainder[0]),int(cursorPos[1]+mouseDiff[1]+remainder[1]),0,0)
			
			remainder=(((cursorPos[0]+mouseDiff[0]+remainder[0])-int(cursorPos[0]+mouseDiff[0]+remainder[0])),
						((cursorPos[1]+mouseDiff[1]+remainder[1])-int(cursorPos[1]+mouseDiff[1]+remainder[1])))
			# print(normal[0],normal[1])
			# print(joyNorm[0],joyNorm[1])
			# print(joyDiff[0],joyDiff[1])
		except Exception:
			print "could not get cursor position"
	# Draw the item at the proper coordinates
	#draw_item(screen,x_coord,y_coord)	   
	 
	#pygame.display.flip()
	#clock.tick(40)
	sleep(.01)

pygame.quit ()
