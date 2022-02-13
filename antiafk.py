import pyautogui as gui
import sys
import time
import pydirectinput as di
import win32gui

def getGameWindow(windowTitle):
  gameWindow = gui.getWindowsWithTitle(windowTitle)
  if len(gameWindow) == 0:
    print(f"Please start {windowTitle}")
    sys.exit(-1)
  for window in gameWindow:
    if windowTitle in window.title:
      game = window
      print(game)
      break
  return game

# wip - works but is not perfect 
# char still moves with a couple px on the y axis each iteration
# shouldn't be a problem in a town and if you don't move at small intervals
def reset(r, x, y, button):
  offset = 20
  nx = x
  ny = y + offset 
  di.click(nx, ny, button=button)
  print(f"Move back (position: {nx}x{ny})")

def rotate(r, x, y, button, reverse = False):
  pos = [
    [x + r, y],
    [x, y - r],
    [x - r, y],
    [x, y + r],
  ]
  if reverse:
    pos.reverse()

  for p in pos:
    di.click(p[0], p[1], button=button)


def focus(game):
  if game.visible is False:
    print("Game window isn't visible. Restoring...")
    game.restore()
  if game.isActive is False:
    print("Game window isn't active.")
    game.activate()


r = 200
# in mins
afkTimer = 1  


if __name__ == '__main__':
  game = getGameWindow("LOST ARK")
  while True:
    prevActiveWindowTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    print(f"Previous window: {prevActiveWindowTitle}")
    focus(game)
    center = {
      "x" : game.left + int(game.width / 2),
      "y" : game.top + int(game.height / 2),
    }
    for i in range(4):
      rotate(r, center["x"], center["y"], di.SECONDARY, reverse=True)

    reset(r, center["x"], center["y"], di.SECONDARY)
    
    print(f"Switch back to previous active window ({prevActiveWindowTitle})")
    prevWindows= gui.getWindowsWithTitle(prevActiveWindowTitle)
    if len(prevWindows) > 0:
      prevWindows[0].activate()

    time.sleep(afkTimer * 60)