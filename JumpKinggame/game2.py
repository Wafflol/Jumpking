import asyncio
import json
import os
from pyppeteer import launch
from time import sleep
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import morphology
showlevel = False
Render = False
player = ['1', '2', '3', '4', '5', 'ArrowLeft', 'ArrowRight']
jump = ['0', '1', '2', '3', '4', '5']
move = ['ArrowLeft', 'ArrowRight']
class Game:
    def __init__(self):
        self.map_mat = np.zeros((900,1200))
        self.playerPosition = [600, 755]
        self.level = 0
        self.lineBoundaries = []
        self.value = 0
        
    global setData
    def setData(self, playerpos, level):
        self.playerPosition = playerpos
        self.level = level
        pass
        
    global setMetadata
    def setMetadata(playerPos, lines, lev):
        sleep(0.1)
        print('player position: ', str(playerPos))
        print('lines: ', str(lines))
        global lineBoundaries
        global PlayerPosition
        global Level
        PlayerPosition = playerPos
        # lineBoundaries = lines
        Level = lev
        # setData(PlayerPosition, Level)
        # self.playerPosition = playerPos
        lineBoundaries = lines
        # self.level = lev
        print("hello", PlayerPosition)

    
    def setRenderMode(self, renderMode):
        if renderMode == 'human':
            Render = True
        else:
            Render = False
        pass
    
    # global printlevel
    def printlevel(output):
        print(output)
        pass
        

    async def obs(self):
        #await page.keyboard.press('L')
        await page.keyboard.press('L')
        await page.waitFor(200)
        await self.setMatrix()
        #await page.evaluate('sendLineData')
        await page.waitFor(200)
        await self.setdatacorrectly()
        sleep(0.1)
        return {"boundaries": np.asarray(self.map_mat.astype(np.uint8)), "player": self.playerPosition, "level": self.level}

    def returnLevelAndPos(self):
        return {"level": self.level, "player": self.playerPosition}
    
    async def getState(self):
        await page.evaluate('sendLineData')

    
    async def startGame(self, RenderMode):
        global server_process   
        global browser
        global page 
        Render = RenderMode
        server_process = subprocess.Popen(['php', '-S', 'localhost:8000', '-t', '/home/wafflol/Downloads/JumpKing/JumpKingAgent/JumpKinggame'],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)                
                
        #print("launching")
        browser = await launch(headless = not Render, ignoreHTTPSErrors=True, args=['--no-sandbox', '--window-size=1920,1080'])
        #print("launched")
        page = await browser.newPage()
        await page.exposeFunction("sendOutput", setMetadata)
        await page.exposeFunction("printCurrentLevel", self.printlevel)
        #print("creating new page")
        await page.goto('http://localhost:8000')
        #print("went to website")
        await page.emulate({'viewport': {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1, 'isMobile': False}, 'screen': {'width': 1200, 'height': 950, 'deviceScaleFactor': 1}})
        
        # debugging stuff
        # print("pressing L")
        # await page.waitFor(1000)
        # await page.keyboard.press('N') 
        await page.waitFor(100)
        await page.keyboard.press('L')    
        await page.evaluate('sendLineData')
        # await page.waitFor(5000)
        # #await page.screenshot({'path': 'screenshot.png'})
        
        
        # print("done")
    
        
        # self.map_mat = np.zeros((900,1200))
    
        # for boundary in lineBoundaries:
        #     start_x, start_y = boundary[0]
        #     end_x, end_y = boundary[1]

        #     # Calculate the coordinates between start and end points
        #     x_coords = np.arange(start_x, end_x + 1)
        #     y_coords = np.arange(start_y, end_y + 1)

        #     # Ensure that the coordinates are within the matrix boundaries
        #     x_coords = np.clip(x_coords, 0, 1199)
        #     y_coords = np.clip(y_coords, 0, 899)

        #     # Mark the coordinates as obstacles
        #     self.map_mat[y_coords, x_coords] = 1
            
        # # fill in missing 1's
        # filled_matrix = self.map_mat.copy()
        # morp_structure = morphology.generate_binary_structure(2, 2)
        # filled_matrix = morphology.binary_fill_holes(filled_matrix, morp_structure).astype(int)
        # self.map_mat = np.logical_or(self.map_mat, filled_matrix).astype(int)
        
        # #remove bottom row and add top row of 1's
        # self.map_mat[899, :] = 0
        # self.map_mat[0, :] = 1

        # # fill in missing 1's
        # filled_matrix = self.map_mat.copy()
        # morp_structure = morphology.generate_binary_structure(2, 2)
        # filled_matrix = morphology.binary_fill_holes(filled_matrix, morp_structure).astype(int)
        # self.map_mat = np.logical_or(self.map_mat, filled_matrix).astype(int)
        
        # #remove top row
        # self.map_mat[0, :] = 0
        
        # if showlevel:
        #     fig, ax = plt.subplots()
        #     ax.imshow(self.map_mat, cmap='binary', vmin=0, vmax=1)
        #     plt.show()
            
            # DONT KNOW IF THIS WORKS, COULD VERY MUCH BE BROKEN
    
    async def terminate(self):
        await browser.close()
        server_process.terminate()
        pass
        
    async def testRun(self):
        await page.waitFor(1000)
        await page.keyboard.press('N') 
        await page.waitFor(100)
        await page.keyboard.press('L')    
        await page.waitFor(5000)
        #await page.screenshot({'path': 'screenshot.png'})
        
        
        print("done")
    
        
        self.map_mat = np.zeros((900,1200))
    
        for boundary in self.lineBoundaries:
            start_x, start_y = boundary[0]
            end_x, end_y = boundary[1]

            # Calculate the coordinates between start and end points
            x_coords = np.arange(start_x, end_x + 1)
            y_coords = np.arange(start_y, end_y + 1)

            # Ensure that the coordinates are within the matrix boundaries
            x_coords = np.clip(x_coords, 0, 1199)
            y_coords = np.clip(y_coords, 0, 899)

            # Mark the coordinates as obstacles
            self.map_mat[y_coords, x_coords] = 1
            
        # fill in missing 1's
        filled_matrix = self.map_mat.copy()
        morp_structure = morphology.generate_binary_structure(2, 2)
        filled_matrix = morphology.binary_fill_holes(filled_matrix, morp_structure).astype(int)
        self.map_mat = np.logical_or(self.map_mat, filled_matrix).astype(int)
        
        #remove bottom row and add top row of 1's
        self.map_mat[899, :] = 0
        self.map_mat[0, :] = 1

        # fill in missing 1's
        filled_matrix = self.map_mat.copy()
        morp_structure = morphology.generate_binary_structure(2, 2)
        filled_matrix = morphology.binary_fill_holes(filled_matrix, morp_structure).astype(int)
        self.map_mat = np.logical_or(self.map_mat, filled_matrix).astype(int)
        
        #remove top row
        self.map_mat[0, :] = 0
        
        if showlevel:
            fig, ax = plt.subplots()
            ax.imshow(self.map_mat, cmap='binary', vmin=0, vmax=1)
            plt.show()
        pass
        
    async def setMatrix(self):
        self.map_mat = np.zeros((900,1200))
    
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
            self.map_mat[y_coords, x_coords] = 1
            
        # fill in missing 1's
        filled_matrix = self.map_mat.copy()
        morp_structure = morphology.generate_binary_structure(2, 2)
        filled_matrix = morphology.binary_fill_holes(filled_matrix, morp_structure).astype(int)
        self.map_mat = np.logical_or(self.map_mat, filled_matrix).astype(int)
        
        #remove bottom row and add top row of 1's
        self.map_mat[899, :] = 0
        self.map_mat[0, :] = 1

        # fill in missing 1's
        filled_matrix = self.map_mat.copy()
        morp_structure = morphology.generate_binary_structure(2, 2)
        filled_matrix = morphology.binary_fill_holes(filled_matrix, morp_structure).astype(int)
        self.map_mat = np.logical_or(self.map_mat, filled_matrix).astype(int)
        
        #remove top row
        self.map_mat[0, :] = 0
        
        if showlevel:
            fig, ax = plt.subplots()
            ax.imshow(self.map_mat, cmap='binary', vmin=0, vmax=1)
            plt.show()
        pass    
        
    async def sendInput(self, input):
        await page.keyboard.press(input) 
        pass 
    
        
    async def playerInput(self, mode, input):
        if mode == "keydown":
            await page.keyboard.down(input)  
        else:
            await page.keyboard.up(input)  
        pass
    
    async def setdatacorrectly(self):
        self.playerPosition = PlayerPosition
        self.level = Level
            
    async def reward(self):
        prevlevel = self.level
        previousYLevel = self.playerPosition[1]
        try:
            # await self.playerInput("keydown", 'L')
            await self.sendInput("L")
            await self.setdatacorrectly()

        except Exception:
            print(Exception) 
        if self.level > prevlevel:
            return 1.0
        elif self.level == prevlevel:
            return 0.0
        else:
            return -1.0
    
    async def action(self, keys):
        keys = np.asarray(keys)
        # for k in range(len(keys)):
            # if(keys[k] == 1):
            #     self.playerInput("keydown", player[k])
            # else:
            #     self.playerInput("keyup", player[k])
        await self.sendInput(jump[keys[0]])
        if keys[1] == 0:
            await self.playerInput("keyup", move[1])
            await self.playerInput("keydown", move[0])
        else:
            await self.playerInput("keyup", move[0])
            await self.playerInput("keydown", move[1])
        pass
            
        
    async def sendUp(self):
        await page.waitFor(1000)
        await self.playerInput("asdf", '5')
        await page.waitFor(10000)        
        pass
    
    async def reset(self):
        await self.sendInput('M')
        await self.playerInput("keydown", 'L')
        await page.waitFor(1000)
        pass
    
        
if __name__ == "__main__":
    obj = Game()
    sleep(0.1)
    asyncio.get_event_loop().run_until_complete(obj.startGame(True))
    asyncio.get_event_loop().run_until_complete(obj.testRun())
    sleep(1)
    #asyncio.get_event_loop().run_until_complete(obj.action([5, 1]))
    # loop.run_until_complete(obj.playerInput("keydown", 'N'))
    # loop.run_until_complete(obj.playerInput("keydown", 'N'))
    # loop.run_until_complete(obj.playerInput("keydown", 'N'))
    asyncio.get_event_loop().run_until_complete(obj.sendInput('N'))
    #sleep(1)
    #asyncio.get_event_loop().run_until_complete(obj.getState())
    # loop.run_until_complete(obj.playerInput("keyup", 'L'))
    # asyncio.get_event_loop().run_until_complete(obj.sendInput('L'))
    sleep(1)
    #loop.run_until_complete(obj.setdatacorrectly())
    # print(obj.returnLevelAndPos())
    print(asyncio.get_event_loop().run_until_complete(obj.obs()))
    asyncio.get_event_loop().run_until_complete(obj.terminate())

