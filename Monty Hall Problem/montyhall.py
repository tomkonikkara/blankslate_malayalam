# Simple pygame program

# Import and initialize the pygame library
import random
import pygame
pygame.init()

NUM_CUPS = 3
NUM_ITERATIONS = 100
SWAP_FLAG = True

# Set up the drawing window
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('MontyHall Problem Demo')
font = pygame.font.Font('freesansbold.ttf', 32)

cupImg_width = 120
cupImg_height = 181
gap_btw_cups = (screen_width - (NUM_CUPS*cupImg_width))//7
cupImg = pygame.image.load('papercup_small.png')
handImg = pygame.image.load('hand_point.png')
cashImg = pygame.image.load('cash.png')
running = True
state = 'Initial'
state_time = {'ShowCups':500,'HandPoint':1000,'LiftCups':1500,'ShowOnlyTwoCups':2000,'ShowCash':3000,'Initial':4000}
winCount = 0
loseCount = 0
ini = True
trialCount = 0
exitState = False

def montyhall_n(n=3,iterations=100,swap = False):
    s = ['Cash'] + ['None'] * (n - 1)
    for i in range(iterations):
        random.shuffle(s)
        idxs = list(range(n))
        idxs2 = list(range(n))
        opened_idxs = None

        selected_idx = random.randint(0,n-1)
        idxs.remove(selected_idx)
        for idx in idxs:
            if s[idx] == 'Cash':
                idxs.remove(idx)
        if len(idxs) == n-2: #If selected is not King
            opened_idxs = idxs[:]
        elif len(idxs) == n-1: # if selected is King
            idx_not_open = random.choice(idxs)
            idxs.remove(idx_not_open)
            opened_idxs = idxs[:]

        idxs2.remove(selected_idx)
        for opened_idx in opened_idxs:
            idxs2.remove(opened_idx)
        swapped_idx = idxs2[0]

        if s[swapped_idx] == 'Cash':
            king_idx = swapped_idx
            winSts = swap
        if s[selected_idx] == 'Cash':
            king_idx = selected_idx
            winSts = not swap

        yield (selected_idx+1, [i+1 for i in opened_idxs],king_idx+1,winSts)

def lift_cup(y_init):
    y_new = y_init
    for i in range(10):
        y_new = y_init - (i*10)
        yield y_new
    while True:
        yield y_new


mo = montyhall_n(n=NUM_CUPS,iterations = NUM_ITERATIONS,swap=SWAP_FLAG)
# Run until the user asks to quit
while running:
    # creates time delay of 10ms
    pygame.time.delay(10)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    if state == 'Initial':
        y_init = (screen_height - cupImg_height) // 2
        y_gen = lift_cup(y_init)
        y2_gen = lift_cup(y_init)
        state = 'ShowCups'
        start_ticks = pygame.time.get_ticks()
        try:
            chosen_cup, lift_cups, cash_cup, winSts = next(mo)
            trialCount += 1
        except StopIteration:
            exitState = True
        ini = True

    #state switcher
    curr_ticks = pygame.time.get_ticks()
    if not exitState:
        for st,st_t in state_time.items():
            if (curr_ticks - start_ticks) > st_t:
                state = st
    else:
        state = 'ExistState'

    #Show score
    text1 = font.render('#Trials : '+"{0}/{1}".format(trialCount,NUM_ITERATIONS), True, (0, 255, 0), (255, 255, 255))
    text2 = font.render('Change decision : ' + ("Yes" if SWAP_FLAG is True else "No"), True, (0, 255, 0), (255, 255, 255))
    text3 = font.render('#Win   : ' + str(winCount)+" ({:.2f}%)".format((winCount/trialCount)*100), True, (255, 0, 0), (255, 255, 255))
    text4 = font.render('#Loss : ' + str(loseCount)+" ({:.2f}%)".format((loseCount/trialCount)*100), True, (255, 0, 0), (255, 255, 255))
    screen.blit(text1, (10, 20))
    screen.blit(text2, (300, 20))
    screen.blit(text3, (screen_width - 320, 20))
    screen.blit(text4, (screen_width - 320, 70))

    if state == 'ShowCups':
        # Draw cup initially

        for i in range(NUM_CUPS):
            x = gap_btw_cups + (cupImg_width + gap_btw_cups) * i
            y = y_init
            screen.blit(cupImg, (x, y))
    elif state == 'HandPoint':
        #Draw cups
        y_init = (screen_height - cupImg_height) // 2
        for i in range(NUM_CUPS):
            x = gap_btw_cups + (cupImg_width + gap_btw_cups) * i
            y = y_init
            screen.blit(cupImg, (x, y))
        # drawing pointing hand
        x = gap_btw_cups + (cupImg_width + gap_btw_cups) * (chosen_cup-1)
        y = ((screen_height + cupImg_height) // 2)
        screen.blit(handImg, (x, y))
    elif state == 'LiftCups':
        #Animate cups
        y_new = next(y_gen)
        for i in range(NUM_CUPS):
            x = gap_btw_cups + (cupImg_width + gap_btw_cups) * i
            if i+1 in lift_cups:
                y = y_new
            else:
                y = y_init
            screen.blit(cupImg, (x, y))
        # drawing pointing hand
        x = gap_btw_cups + (cupImg_width + gap_btw_cups) * (chosen_cup - 1)
        y = ((screen_height + cupImg_height) // 2)
        screen.blit(handImg, (x, y))
    elif state == 'ShowOnlyTwoCups':
        #Show Cups
        for i in range(NUM_CUPS):
            x = gap_btw_cups+(cupImg_width+gap_btw_cups)*i
            if i+1 not in lift_cups:
                screen.blit(cupImg, (x, y_init))
        # drawing pointing hand
        x = gap_btw_cups + (cupImg_width + gap_btw_cups) * (chosen_cup - 1)
        y = ((screen_height + cupImg_height) // 2)
        screen.blit(handImg, (x, y))
    elif state == 'ShowCash':
        # Animate cups
        y_new = next(y2_gen)
        for i in range(NUM_CUPS):
            x = gap_btw_cups + (cupImg_width + gap_btw_cups) * i
            if i + 1 == cash_cup:
                screen.blit(cashImg, (x, y_init))
            if i + 1 not in lift_cups:
                y = y_new
                screen.blit(cupImg, (x, y))
        #Update score
        if ini:
            winCount += int(winSts)
            loseCount += int(not winSts)
        ini = False
        # drawing pointing hand
        x = gap_btw_cups + (cupImg_width + gap_btw_cups) * (chosen_cup - 1)
        y = ((screen_height + cupImg_height) // 2)
        screen.blit(handImg, (x, y))
    elif state == 'ExistState':
        #Show Score
        screen.blit(text1, (10, 20))
        screen.blit(text2, (300, 20))
        screen.blit(text3, (screen_width - 320, 20))
        screen.blit(text4, (screen_width - 320, 70))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()