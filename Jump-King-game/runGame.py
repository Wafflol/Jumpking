import asyncio
import os
from pyppeteer import launch
from time import sleep
import subprocess


print(os.getcwd())


async def main():
    subprocess.call(['sh', './Jump-King-game/Run.sh'])

    while True:
        try:
            reader, writer = await asyncio.open_connection('localhost', 8000)
            writer.close()
            break
        except ConnectionRefusedError:
            await asyncio.sleep(5)  # Increase delay to give server more time to start up
    #print("launching")
    browser = await launch(headless=False, ignoreHTTPSErrors=True, args=['--no-sandbox', '--window-size=1920,1080'])
    #print("launched")
    page = await browser.newPage()
    #print("creating new page")
    await page.goto('http://localhost:8000')
    #print("went to website")
    await page.emulate({'viewport': {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1, 'isMobile': False}, 'screen': {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1}})
    await page.keyboard.press('L')
    await page.waitFor(5000)
    await page.screenshot({'path': 'screenshot.png'})
    await browser.close()
    #server_process.terminate()

asyncio.get_event_loop().run_until_complete(main())