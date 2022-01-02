from psychopy import core, visual, gui, data, event
import time, numpy, random, os, sys

def pSetList(L):
	L2 = L[:]
	a = L2.pop(14) #Removes 'O'
	b = L2.pop(12) #Removes 'M'
	c = L2
	return(a, b, c)
def SetList(L): #Input: list; copy, shuffle; Output: 2 values: 1st item & following items as a list
	L2 = L[:] #Creates copy of list
	random.shuffle(L2)
	a, b = L2[0], L2[1:] #a is assigned a letter w/o brackets; b is assigned a list w/ brackets
	return(a, b)
def RandSlot(a,b): #Generates a random number in a range
	return(random.randrange(a, b))
def weighted_choice(weights): #Input: list of numbers; Output: list position determined by argument; list starts at 0
	totals = numpy.cumsum(weights) #Calculates cumulative sum of items in list
	final_total = totals[-1] #Selects last item in list
	throw = numpy.random.rand()*final_total #Return product: rand float pt num in range (0.0, 1.0) & cumultv sum
	return numpy.searchsorted(totals, throw)
def Lpos_counter(lag, a, b, c, d, e, f): #Input: number, c1-6; Output: updated c1-6
	if lag == 1:
		a += 1
	elif lag == 2:
		b += 1
	elif lag == 3:
		c += 1
	elif lag == 4:
		d += 1
	elif lag == 5:
		e += 1
	elif lag == 6:
		f += 1
	return(a, b, c, d, e, f)
def Fixation(a, b, c): #Presents fixation cross
	win.flip(); core.wait(a)
	fix.draw(); win.flip(); core.wait(b)
	win.flip(); core.wait(c)
def Letters(a, b): #Presents letter stimuli
	stim.draw()
	L0 = globalClock.getTime()
	win.flip(); core.wait(a)
	L1 = globalClock.getTime()
	win.flip(); core.wait(b)
	L2 = globalClock.getTime()
	stime, isitime, functime = (L1-L0), (L2-L1), (L2-L0)
	return(stime, isitime, functime)
def KeyPrompt_Response(t): #Input: keypress, target; Output: match     LATER --> rt
	visual.TextStim(win, text=pt, color='black', pos=[0,0]).draw()
	win.flip()
	key = event.waitKeys(keyList=None)
	converted_key = key[0].upper() #Removes list bracket from keypress & converts to uppercase
	if converted_key == 'ESCAPE':
		core.quit()
	elif converted_key == t:
		match = 'Correct'
	else:
		match = 'Incorrect'
	win.flip()
	return(converted_key, match)
	event.clearEvents() #must clear other (eg mouse) events - they clog the buffer
def Short_Break():
	sb, re = "Please take a short break!", "Press any key to return to the experiment."
	visual.TextStim(win, text=sb, color='black', pos=[0,0]).draw()
	win.flip()
	core.wait(4.0)
	visual.TextStim(win, text=re, color='black', pos=[0,0]).draw()
	win.flip()
	key = event.waitKeys(keyList=None)
	converted_key = key[0].upper()
	if converted_key == 'ESCAPE':
		core.quit()
	win.flip()
def End_message():
	em = "The experiment is now over.\n\nThank you for your participation."
	visual.TextStim(win, text=em, color='black', pos=[0,0]).draw()
	win.flip()
	core.wait(2.5)

#path = "D:\SkyDrive\2013 Winter Term\- Psych 499 - Thesis\Python Scripts"
#os.path.dirname(os.path.abspath(sys.argv[0]))
path = "/usr/local/protocol/attnBlnk/data/"
os.chdir(path)

expInfo = {'dateStr':data.getDateStr(), 'Subject':''} #Set parameters (date, subject)
dlg = gui.DlgFromDict(expInfo, title='RSVP Exp', fixed=['dateStr']) #Presents dialogue
if dlg.OK:
	subj = expInfo['Subject']
	fileName = subj + expInfo['dateStr']
	dataFile = open(fileName +'.csv', 'w') #Text w/ 'comma-separated-values'
	dataFile.write('Trial #,T1pos,Lpos,T2pos,T1,T2,kp1,kp2,T1_match,T2_match,global,s,isi,isd,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,A23\n') #Headings
else:
	core.quit()

win = visual.Window(size=(1024,768), pos=None, color="gray", fullscr=True, waitBlanking=False, monitor = "brittlab1")
fix = visual.ShapeStim(win, lineColor='black', lineWidth=3.0, vertices=((-0.08, 0), (0.08, 0), (0,0), (0,0.08), (0,-0.08)), interpolate=False, closeShape=False, pos=(0,0)) #Fixation cross
palpha = ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
pbeta = ["A", "B", "C"]
alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"]
beta = ["X", "Y", "Z"]
earliestT1, latestT1 = 3, 7 #Yields 3-6, but list starts at 0 so list position will be 4-7
earliestLpos, latestLpos = 1, 7 #Yields 1-6
T2_wprob = [1, 5, 1, 1, 1, 1] #Weighted probabilities; weights don't need to sum to any num
c1, c2, c3, c4, c5, c6 = 0, 0, 0, 0, 0, 0 #Counter: T2 lag position
noT_wprob = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #Yields nums 1-10
noT1_counter, noT2_counter = 0, 0
b4fix, fixtime, afterfix = 0.05, 0.18, 0.05 #Fixation times (in s)
Stimtime, ISItime = 0.077, 0.009 #Windows: 0.077, 0.009 (82.7ms, 15.5ms); Linux: 0.083, 0.005
ptrial, pmax = 0, 5
trial, max =  0, 20
halfmax = max/2

initial_msg = visual.TextStim(win, text='You will be shown a sequence of letters. Your task is to identify the target letters.\n\nPress any key when ready.', color='black', pos=[0,0]).draw()
win.flip()
event.waitKeys() #Pause until keypress
globalClock = core.Clock()

practice_msg = visual.TextStim(win, text="We will begin with some practice trials.\n\nThe 1st target will be a white letter and the 2nd target will either be a black 'A', 'B', or 'C' \n\nPress any key when ready.", color='black', pos=[0,0]).draw()
win.flip()
event.waitKeys()

while ptrial < pmax:
	T1, A = SetList(palpha)
	T2, discard = SetList(pbeta)
	T1pos = RandSlot(earliestT1, latestT1)
	Lpos = RandSlot(earliestLpos, latestLpos)
	T2pos = T1pos + Lpos
	A.insert(T1pos, T1)
	A.insert(T2pos, T2)
	lenA = len(A)
	zipper = zip(A, range(lenA))
	
	Fixation(b4fix, fixtime, afterfix) #Presents fixation cross
	tlen = 0
	for st, i in zipper:
		if tlen == 16: #Breaks out of smallest enclosing for or while loop
			break
		if i == T1pos:
			sc = 'white'
		elif i == T2pos:
			sc = 'black'
		else:
			sc = 'black'
		stim = visual.TextStim(win, text=st, pos=[0,0], height=0.5, color=sc) #Letter stimulus
		s, isi, isd = Letters(Stimtime, ISItime) #Presents letter stimuli
		tlen += 1
	
	pt = "What was target letter 1?"
	kp1, T1_match = KeyPrompt_Response(T1)
	pt = "What was target letter 2?"
	kp2, T2_match = KeyPrompt_Response(T2)
	
	core.wait(.5)
	ptrial += 1

start_msg = visual.TextStim(win, text="We will now begin the experiment.\n\nThe 1st target will be a white letter and the 2nd target will either be a black 'X', 'Y', or 'Z' \n\nPress any key when ready.", color='black', pos=[0,0]).draw()
win.flip()
event.waitKeys()
globalClock.reset(newT=0.0)

while trial < max:
	T1, A = SetList(alpha)
	T2, discard = SetList(beta)
	T1pos = RandSlot(earliestT1, latestT1) #Assigns 3-6 to a var (pos 4-7)
	Lpos = weighted_choice(T2_wprob)+1 #+1 b/c list starts at 0
	T2pos = T1pos + Lpos

	noT = weighted_choice(noT_wprob)+1 #+1 b/c list starts at 0
	if noT == 1: #No T1 will appear
		A[T2pos] = T2 #Replaces T2 at spec position
		T1, T1pos = 'SPACE', None
		noT1_counter += 1
	elif noT == 2: #No T2 will appear
		A.insert(T1pos, T1) #Inserts T1 at spec position
		T2, Lpos, T2pos = 'SPACE', None, None
		noT2_counter += 1
	else:
		A.insert(T1pos, T1) #Inserts T1 at spec position
		A[T2pos] = T2 #Replaces T2 at spec position
		c1, c2, c3, c4, c5, c6 = Lpos_counter(Lpos, c1, c2, c3, c4, c5, c6)

	lenA = len(A) #Final length of letter list (including T1 = 23 + T2 = 24)
	zipper = zip(A, range(lenA)) #Assigns a number to each element in list

	globalt = globalClock.getTime()
	Fixation(b4fix, fixtime, afterfix) #Presents fixation cross
	tlen = 0 #Trial length (Total number of: letters, T1, T2)
	for st, i in zipper:
		if tlen == 16: #Breaks out of smallest enclosing for or while loop
			break
		if i == T1pos:
			sc = 'white'
		elif i == T2pos:
			sc = 'black'
		else:
			sc = 'black'
		stim = visual.TextStim(win, text=st, pos=[0,0], height=0.5, color=sc) #Letter stimulus
		s, isi, isd = Letters(Stimtime, ISItime) #Presents letter stimuli
		tlen += 1

	pt = "What was target letter 1?"
	kp1, T1_match = KeyPrompt_Response(T1)
	pt = "What was target letter 2?"
	kp2, T2_match = KeyPrompt_Response(T2)

	core.wait(.5)
	trial +=1
	dataFile.write('%i,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (trial,T1pos,Lpos,T2pos,T1,T2,kp1,kp2,T1_match,T2_match,globalt,s,isi,isd,A))
	if trial == halfmax:
		Short_Break()
	elif trial == max:
		End_message()

ctot = c1+c2+c3+c4+c5+c6
dataFile.write("Total Trials, T1 absent, T2 absent\n%i,%i,%i\n" % (trial, noT1_counter, noT2_counter))
dataFile.write("Lpos_c1, Lpos_c2, Lpos_c3, Lpos_c4, Lpos_c5, Lpos_c6, Lpos_ctot\n%i,%i,%i,%i,%i,%i,%i\n" % (c1, c2, c3, c4, c5, c6, ctot))

dataFile.close()
