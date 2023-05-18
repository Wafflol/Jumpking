import asyncio
import os
from pyppeteer import launch
from time import sleep
import subprocess
#import startWebpage


#print(os.getcwd())

def hello(playerPos, lines):
        print('player position: ', str(playerPos))
        print('lines: ', str(lines))

    # Expose the callback function to the window object in the page

async def main():        
    server_process = subprocess.Popen(['php', '-S', 'localhost:8000', '-t', '/home/wafflol/Downloads/JumpKingAgent/Jump-King-game'],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)                
            
    #print("launching")
    browser = await launch(headless=True, ignoreHTTPSErrors=True, args=['--no-sandbox', '--window-size=1920,1080'])
    #print("launched")
    page = await browser.newPage()    
    await page.exposeFunction("sendOutput", hello)
    #print("creating new page")
    await page.goto('http://localhost:8000')
    #print("went to website")
    await page.emulate({'viewport': {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1, 'isMobile': False}, 'screen': {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1}})
    print("pressing L")
    await page.waitFor(1000)
    await page.keyboard.press('L')    
    await page.waitFor(5000)
    await page.screenshot({'path': 'screenshot.png'})
    await browser.close()
    print("done")
    
    server_process.terminate()

asyncio.get_event_loop().run_until_complete(main())
