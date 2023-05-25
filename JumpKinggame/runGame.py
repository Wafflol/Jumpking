import asyncio
import os
from pyppeteer import launch
from time import sleep
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import morphology
print(os.getcwd())

def hello(playerPos, lines, lev):
        print('player position: ', str(playerPos))
        print('lines: ', str(lines))
        #print(lines)
        global lineBoundaries
        global playerPosition
        global level
        playerPosition = playerPos
        lineBoundaries = lines
        level = lev

    # Expose the callback function to the window object in the page

async def main():        
    server_process = subprocess.Popen(['php', '-S', 'localhost:8000', '-t', '/home/wafflol/Downloads/JumpKing/JumpKingAgent/JumpKinggame'],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)                
            
    #print("launching")
    browser = await launch(headless=False, ignoreHTTPSErrors=True, args=['--no-sandbox', '--window-size=1920,1080'])
    #print("launched")
    page = await browser.newPage()    
    await page.exposeFunction("sendOutput", hello)
    #print("creating new page")
    await page.goto('http://localhost:8000')
    #print("went to website")
    await page.emulate({'viewport': {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1, 'isMobile': False}, 'screen': {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1}})
    print("pressing L")
    await page.waitFor(1000)
    await page.keyboard.press('N') 
    await page.waitFor(100)
    await page.keyboard.press('N') 
    await page.waitFor(100)
    await page.keyboard.press('N') 
    await page.waitFor(100)
    await page.keyboard.press('L')
    print("pressed")
    await page.waitFor(1000)
    await page.screenshot({'path': 'screenshot.png'})
    await browser.close()
    print("done")
    
    server_process.terminate()
    
    map_mat = np.zeros((900,1200))
    
    for boundary in lineBoundaries:
        start_x, start_y = boundary[0]
        end_x, end_y = boundary[1]

        # Calculate the coordinates between start and end points
        x_coords = np.arange(start_x, end_x + 1)
        y_coords = np.arange(start_y, end_y + 1)

        # Ensure that the coordinates are within the matrix boundaries
        x_coords = np.clip(x_coords, 0, 1199)
        y_coords = np.clip(y_coords, 0, 899)

        # Mark the coordinates as obstacles
        map_mat[y_coords, x_coords] = 1
        

    # Create a copy of the matrix
    filled_matrix = map_mat.copy()

    # Use binary fill to fill the enclosed areas
    morp_structure = morphology.generate_binary_structure(2, 2)
    filled_matrix = morphology.binary_fill_holes(filled_matrix, morp_structure).astype(int)

    # Update the matrix with the filled areas
    map_mat = np.logical_or(map_mat, filled_matrix).astype(int)
    
    
    fig, ax = plt.subplots()
    ax.imshow(map_mat, cmap='binary', vmin=0, vmax=1)
    plt.show()
    
    
asyncio.get_event_loop().run_until_complete(main())
