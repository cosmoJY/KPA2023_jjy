# [한국심리학회] 프로그래밍 도구, 화면 재생 빈도, 운영체제에 따른 시각 자극 제시 정확도 비교
# 문의: word3276@gmail.com

# PsychoPy 2023.1.3 & Python 3.8
# 절차: 입력창에 파라미터 입력 > 'Press Z' 문구가 뜨면 z키(블록 1) > 자극 제시 후 스페이스바(16회 반복)
#       > 'Press Z' 문구가 뜨면 z키(블록 2) > ... > 블록 15가 끝나면 자동 종료
# 측정 데이터파일 경로: [result] 폴더
#     데이터파일 변인명: 1. ID  2. 블록번호  3. 시행번호  4. 운영체제  5. PC종류  6. 화면 재생 빈도(hz)  
#                   7. 코드: while[1]/개발자[2] 8. 지연요소: 없음[0]/키입력직후[1]/반복문[2]
#                   9. 자극 제시시간(의도)  10. 자극 지속시간(프로그램)  11. 검은화면 지속시간(프로그램)

# Configuration settings -----------------------------------------
from psychopy import visual, core, event, data, gui, logging, monitors, tools, parallel #import some libraries from PsychoPy
from psychopy.hardware import keyboard
from psychopy.tools import colorspacetools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray, arctan
from numpy.random import random, randint, normal, shuffle
import random
import os #handy system and path functions
import glob # Filename globbing utility.
from PIL import Image # Get the size(demension) of an images 
import math
logging.console.setLevel(logging.CRITICAL)

screenNumber = 0;         # 모니터 스크린 번호

# Test settings -----------------------------------------
nrepeat = 16
nblock = 15
cblock = [0, math.ceil((nblock/2)-1), (nblock-1)]
    
expName = 'Test'
expInfo = {
    'ID[아무숫자]': '',
    'OS[아무숫자]':'',
    'PC[아무숫자]': '',
    '화면 재생 빈도(hz): 예시[60]': '',
    '자극 제시시간(초): 예시[1/60]' : '',
    '코드: while[3]/개발자[4]': '',
    '지연요소: 없음[0]/키입력직후[1]/반복문[2]' : ''
} 
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
participant = int(expInfo['ID[아무숫자]'])
os = int(expInfo['OS[아무숫자]'])
pc = int(expInfo['PC[아무숫자]'])
hz = int(expInfo['화면 재생 빈도(hz): 예시[60]'])
whilewhen = int(expInfo['코드: while[3]/개발자[4]'])
delay = int(expInfo['지연요소: 없음[0]/키입력직후[1]/반복문[2]'])
target_t = eval(expInfo['자극 제시시간(초): 예시[1/60]'])

slack = 1/hz/2
frameTolerance = 0.001  # how close to onset before 'same' frame

waitClock = core.Clock()
key_resp = keyboard.Keyboard(backend='ptb')
blankClock = core.Clock()
ptargetClock = core.Clock()
pmaskClock = core.Clock()
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
  
location = 2
mask_t = 2/60

if delay != 1:
    blank_t = 6/60
else:
    blank_t = 0

if whilewhen == 2 & delay == 2:
    print('개발자 코드 & 지연요소 반복문 조합은 불가능합니다.')
    core.quit()

# Screen settings -----------------------------------------
monitor_inch = 24; distance_cm = 70; monitorX = 2560; monitorY = 1440;

bgColorRGB = [255,255,255]
black = [0, 0, 0]
red = [255, 0, 0]
  
# create a window
# screen = screenNumber, 
win = visual.Window(size = [monitorX, monitorY], fullscr = True, units='pix', color = bgColorRGB, colorSpace = 'rgb255', multiSample = False)   # anti-aliasing (multiSample = True, numSamples = 16)  # fullscr = 'bool',
win.mouseVisible = False

centerx = 0; centery = 0

# Image & text settings ----------------------------------------
mask = visual.ImageStim(win, image = "stim/900x600_Black.jpg", size = (900, 600), pos = (centerx, centery), units = "pix")
targetName_g = 'stim/900x600_25_100000_green.jpg'
targetName_r = 'stim/900x600_25_100000_magenta.jpg'
target_g = visual.ImageStim(win, image = targetName_g, size = (900, 600), pos = (centerx, centery), units = "pix")
target_r = visual.ImageStim(win, image = targetName_r, size = (900, 600), pos = (centerx, centery), units = "pix")

txtloc_y = centery + 350

text_b = visual.TextStim(win, text= "1", pos = (centerx, txtloc_y), units = 'pix', height = 30, color = bgColorRGB, bold = False)

# Test start ----------------------------------------
timestamp = np.empty((0, 11), int)
for b in range(0, nblock):
    txtcolor = black
    txtinst = '--\nPress Z'
    if delay == 2:
        targetName = targetName_g
    else:
        target = target_g
    for c in cblock:
        if c == b:
            txtcolor = red
            txtinst = 'CAMERA\nPress Z'
            if delay == 2:
                targetName = targetName_r
            else:
                target = target_r
    text0 = visual.TextStim(win, text= txtinst, pos = (centerx, txtloc_y), units = 'pix', height = 30, color = txtcolor, bold = False)
    text0.draw(); win.flip()
    kb = keyboard.Keyboard(backend='ptb')
    kb.clock.reset() 
    keys = kb.waitKeys(keyList=['z'], waitRelease=False)
    for t in range(0, nrepeat):
        tcurrent = t
        if whilewhen == 3:
            text = visual.TextStim(win, text= 'psychopy(while)' +  str(hz) + '_' + str(math.floor(target_t*1000)) + '_' + str(t), pos = (centerx, txtloc_y), units = 'pix', height = 30, color = txtcolor, bold = False)
            
            win.flip()
            kb = keyboard.Keyboard(backend='ptb')
            kb.waitKeys(keyList=['space'], waitRelease=False)
              
            clock_b = core.Clock()
            while clock_b.getTime() < blank_t - slack:
                win.flip()
                
            clock = core.Clock()
            while clock.getTime() < target_t - slack:
                if delay == 2:
                    target = visual.ImageStim(win, image = targetName, size = (900, 600), pos = (centerx, centery), units = "pix")
                target.draw(); text.draw()
                win.flip()
            target_realtime = clock.getTime()
        
            clock_m = core.Clock() 
            while clock_m.getTime() < mask_t - slack:
                mask.draw(); text.draw()
                win.flip()
            mask_realtime = clock_m.getTime()
        if whilewhen == 4:
            text = visual.TextStim(win, text= 'psychopy(when)' +  str(hz) + '_' + str(math.floor(target_t*1000)) + '_' + str(tcurrent), pos = (centerx, txtloc_y), units = 'pix', height = 30, color = txtcolor, bold = False)
            # ------Prepare to start Routine "wait"-------
            continueRoutine = True
            # update component parameters for each repeat
            key_resp.keys = []
            key_resp.rt = []
            _key_resp_allKeys = []
            # keep track of which components have finished
            waitComponents = [key_resp]
            for thisComponent in waitComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            ttime = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            waitClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1  
            # -------Run Routine "wait"-------
            while continueRoutine:
                # get current time
                t = waitClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=waitClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # *key_resp* updates
                waitOnFlip = False
                if key_resp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp.frameNStart = frameN  # exact frame index
                    key_resp.tStart = ttime  # local t and not account for scr refresh
                    key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                    key_resp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
                    _key_resp_allKeys.extend(theseKeys)
                    if len(_key_resp_allKeys):
                        key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                        key_resp.rt = _key_resp_allKeys[-1].rt
                        # a response ends the routine
                        continueRoutine = False
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in waitComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            # -------Ending Routine "wait"-------
            for thisComponent in waitComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "wait" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

            # ------Prepare to start Routine "blank"-------
            continueRoutine = True
            # update component parameters for each repeat
                # keep track of which components have finished
            blankComponents = [text_b]
            for thisComponent in blankComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            ttime = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            blankClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            # -------Run Routine "blank"-------
            while continueRoutine:
                # get current time
                ttime = blankClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=blankClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                 
                # *text_b* updates
                if text_b.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_b.frameNStart = frameN  # exact frame index
                    text_b.tStart = ttime  # local t and not account for scr refresh
                    text_b.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                    text_b.setAutoDraw(True)
                if text_b.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text_b.tStartRefresh + blank_t-frameTolerance:
                        # keep track of stop time/frame for later
                        text_b.tStop = ttime  # not accounting for scr refresh
                        text_b.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(text, 'tStopRefresh')  # time at next scr refresh
                        text_b.setAutoDraw(False)
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in blankComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
            # -------Ending Routine "blank"-------
            for thisComponent in blankComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            blank_realtime = tThisFlipGlobal - text_b.tStartRefresh
            # the Routine "blank" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "ptarget"-------
            continueRoutine = True
            # update component parameters for each repeat
                # keep track of which components have finished
            ptargetComponents = [target, text]
            for thisComponent in ptargetComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            ttime = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            ptargetClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            # -------Run Routine "ptarget"-------
            while continueRoutine:
                # get current time
                ttime = ptargetClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=ptargetClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                 
                # *target* updates
                if target.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    target.frameNStart = frameN  # exact frame index
                    target.tStart = ttime  # local t and not account for scr refresh
                    target.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(target, 'tStartRefresh')  # time at next scr refresh
                    target.setAutoDraw(True)
                if target.status == STARTED:
                    if tThisFlipGlobal > target.tStartRefresh + target_t-frameTolerance:
                        # keep track of stop time/frame for later
                        target.tStop = ttime  # not accounting for scr refresh
                        target.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(target, 'tStopRefresh')  # time at next scr refresh
                        target.setAutoDraw(False) 
                         
                # *text* updates
                if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text.frameNStart = frameN  # exact frame index
                    text.tStart = ttime  # local t and not account for scr refresh
                    text.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                    text.setAutoDraw(True)
                if text.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text.tStartRefresh + target_t-frameTolerance:
                        # keep track of stop time/frame for later
                        text.tStop = ttime  # not accounting for scr refresh
                        text.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(text, 'tStopRefresh')  # time at next scr refresh
                        text.setAutoDraw(False)
                        
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in ptargetComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            # -------Ending Routine "ptarget"-------
            
            for thisComponent in ptargetComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            target_realtime = tThisFlipGlobal - target.tStartRefresh # ptargetClock.getTime()
            # the Routine "ptarget" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "pmask"-------
            continueRoutine = True
            text_2 = text
            # keep track of which components have finished
            pmaskComponents = [mask, text_2]
            for thisComponent in pmaskComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            ttime = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            pmaskClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1  
            # -------Run Routine "pmask"-------
            while continueRoutine:
                # get current time
                ttime = pmaskClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=pmaskClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # *mask* updates
                if mask.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    mask.frameNStart = frameN  # exact frame index
                    mask.tStart = ttime  # local t and not account for scr refresh
                    mask.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask, 'tStartRefresh')  # time at next scr refresh
                    mask.setAutoDraw(True)
                if mask.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask.tStartRefresh + mask_t-frameTolerance:
                        # keep track of stop time/frame for later
                        mask.tStop = ttime  # not accounting for scr refresh
                        mask.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask, 'tStopRefresh')  # time at next scr refresh
                        mask.setAutoDraw(False)
                # *text_2* updates
                if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_2.frameNStart = frameN  # exact frame index
                    text_2.tStart = ttime  # local t and not account for scr refresh
                    text_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
                    text_2.setAutoDraw(True)
                if text_2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text_2.tStartRefresh + mask_t-frameTolerance:
                        # keep track of stop time/frame for later
                        text_2.tStop = ttime  # not accounting for scr refresh
                        text_2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(text_2, 'tStopRefresh')  # time at next scr refresh
                        text_2.setAutoDraw(False)
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in pmaskComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            # -------Ending Routine "pmask"-------
            for thisComponent in pmaskComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            mask_realtime = tThisFlipGlobal - mask.tStartRefresh  #pmaskClock.getTime()
        timestamp  = np.append(timestamp, np.array([[participant, b, tcurrent, os, pc, hz, whilewhen, delay, target_t, target_realtime, mask_realtime]]), axis = 0);  # 행 추가

# Save data file -----------------------------------------------------------
dataFileName='result/PsychoPy(Coder)_' + str(participant) +  '_' + str(os) + '_' + str(pc) + '_' + str(hz) + '_' + str(whilewhen) + '_' + str(delay) + '_' + str(math.floor(target_t*1000)) + '_' + data.getDateStr() + '.txt'
np.savetxt(dataFileName, timestamp, delimiter='\t', fmt='%f')
 
core.quit()