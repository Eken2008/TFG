import tkinter
import json
from PIL import ImageTk
from PIL import Image as PILImage
import math
import time

class TkinterForGames:
    
    def __init__(self):
        self.tkinter = tkinter
        self.window = self.tkinter.Tk()
        self.window.title("Made with tfg: Untitled")
        self.canvas = self.tkinter.Canvas(self.window)
        self.canvas.pack(fill="both", expand=True)#.place(x=0, y=0, anchor = 'nw')

        self.keys = []
        self.specialKeys = []
        self.mouseButtons = []

        self.mousePos = (0, 0)
        self.window.bind("<KeyPress>",self._keyPressed)
        self.window.bind("<KeyRelease>",self._keyReleased)
        self.window.bind('<Motion>', self._mouseChange)
        self.window.bind("<ButtonPress>", self._mouseDown)
        self.window.bind("<ButtonRelease>", self._mouseUp)

        self.mainCamera = Camera(self, Vector2(0,0))
        self.start_time = time.time()
        self.fps = 0
        self.deltaTime = 0

    def resizable(self, resizable : bool):
        if isinstance(resizable, bool):
            self.window.resizable(resizable,resizable)
        else:
            raise TypeError("resizable needs to be a bool")
    
    def fullscreen(self, fullscreen : bool):
        if isinstance(fullscreen, bool):
            self.window.attributes('-fullscreen', fullscreen)
        else:
            raise TypeError("fullscreen needs to be a bool")

    def size(self, width : int, height : int):
        if isinstance(width, int):
            if isinstance(height, int):
                self.window.geometry(f"{width}x{height}")
            else:
                raise TypeError("height needs to be an int")
        else:
            raise TypeError("width needs to be an int")

    def mousePressed(self, button):
        button = str(button)
        if button == "0":
            button = "LMB"
        if button == "1":
            button = "RMB"
        if button == "2":
            button = "MMB"
        return button.upper() in self.mouseButtons

    def _mouseDown(self, event):
        if event.num == 1:
            if not "LMB" in self.mouseButtons:
                self.mouseButtons.append("LMB")
        if event.num == 2:
            if not "MMB" in self.mouseButtons:
                self.mouseButtons.append("MMB")
        if event.num == 3:
            if not "RMB" in self.mouseButtons:
                self.mouseButtons.append("RMB")

    def _mouseUp(self, event):
        if event.num == 1:
            if "LMB" in self.mouseButtons:
                del self.mouseButtons[self.mouseButtons.index("LMB")]
        if event.num == 2:
            if "MMB" in self.mouseButtons:
                del self.mouseButtons[self.mouseButtons.index("MMB")]
        if event.num == 3:
            if "RMB" in self.mouseButtons:
                del self.mouseButtons[self.mouseButtons.index("RMB")]

    def _mouseChange(self, event):
        self.mousePos = (event.x, event.y)

    def _keyPressed(self, event):
        if not event.char in self.keys:
            self.keys.append(event.char)
        if not event.keysym in self.specialKeys:
            self.specialKeys.append(event.keysym)

    def _keyReleased(self, event):
        if event.char in self.keys:
            del self.keys[self.keys.index(event.char)]
        if event.keysym in self.specialKeys:
            del self.specialKeys[self.specialKeys.index(event.keysym)]

    def specialKeyPressed(self, key):
        return key in self.specialKeys

    def keyPressed(self, key):
        return key in self.keys
    

    def getWindow(self):
        return self.window

    def getCanvas(self):
        return self.canvas

    def createScene(self):
        return Scene(self.window)

    def update(self):
        self.window.mainloop()
    
    def render(self, scene):
        try:
            self.fps = 1.0 / (time.time() - self.start_time)
        except:
            self.fps = 0

        self.deltaTime = time.time() - self.start_time

        self.start_time = time.time()

        try:
            self.canvas.delete("all")
            for i in scene.getObjects().GetList():
                i.render()
            self.window.update()
        except tkinter.TclError as e:
            if str(e) != 'invalid command name ".!canvas"':
                print(e)
            exit()
        
        

#tfg = TkinterForGames()
class Scene:
    def __init__(self, tkWindow):
        self.tkWindow = tkWindow
        self.objects = []

    def addObject(self, object):
        if isinstance(object, Object):
            self.objects.append(object)
            object.scene = self
        else:
            raise TypeError(f"{object} {type(object)} is not an instance of Object")
    
    def getObjects(self):
        return ObjectList(self.objects)

class Hitbox:
    def __init__(self):
        #self.width = width
        #self.height = height
        #self.hitboxEvent = None
        #return self
        pass

    #create rectangle collision
    def Rect(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        return self

    def setCollisionEvent(self, function):
        pass

    def checkCollision(self, hitboxB):
        if isinstance(hitboxB, Hitbox):

            if hitboxB.x <= self.x and self.x <= hitboxB.x+hitboxB.width:
                if self.y <= hitboxB.y and hitboxB.y <= self.y+self.height:
                    return True
                if hitboxB.y <= self.y and self.y <= hitboxB.y+hitboxB.height:
                    return True

            if self.x <= hitboxB.x and hitboxB.x < self.x+self.width:
                if self.y <= hitboxB.y and hitboxB.y <= self.y+self.height:
                    return True
                if hitboxB.y <= self.y and self.y <= hitboxB.y+hitboxB.height:
                    return True

            return False

        else:
            raise TypeError(f"hitboxB ({hitboxB}) is not an instance of Hitbox")
        
    def getCollisionPoint(hBoxA, hBoxB, accuracy):
        if accuracy > 0:
            if isinstance(hBoxA, Hitbox):
                if isinstance(hBoxB, Hitbox):
                    hBoxes = []
                    hBoxes.append(Hitbox().Rect(hBoxA.x, hBoxA.y, hBoxA.width/2, hBoxA.height/2))
                    hBoxes.append(Hitbox().Rect(hBoxA.x+hBoxA.width/2, hBoxA.y, hBoxA.width/2, hBoxA.height/2))
                    hBoxes.append(Hitbox().Rect(hBoxA.x, hBoxA.y+hBoxA.height/2, hBoxA.width/2, hBoxA.height/2))
                    hBoxes.append(Hitbox().Rect(hBoxA.x+hBoxA.width/2, hBoxA.y+hBoxA.height/2, hBoxA.width/2, hBoxA.height/2))
                    x = 0
                    for i in range(int(len(hBoxes)/2)):
                        for j in range(2):
                            if hBoxB.checkCollision(hBoxes[x]):
                                if hBoxA.width >= accuracy:
                                    
                                    return Hitbox.getCollisionPoint(hBoxes[x], hBoxB, accuracy)
                                else:
                                    return Vector2(hBoxA.x,hBoxA.y)
                            x+=1
                else:
                    raise TypeError("hBoxB needs to be an instance of Hitbox.")
            else:
                raise TypeError("hBoxA needs to be an instance of Hitbox.")
        else:
            raise ValueError("The accuracy needs to be higher than 0.")

    def getCollisionEvent(self):
        pass

class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def distanceBetween(posA, posB):
        if isinstance(posA, Vector2) or isinstance(posA, tuple):
            if isinstance(posB, Vector2) or isinstance(posB, tuple):
                if type(posA) == tuple:
                    posA = Vector2(posA[0], posA[1])
                if type(posB) == tuple:
                    posB = Vector2(posB[0], posB[1])
                return math.sqrt(math.pow(posA.x-posB.x,2)+math.pow(posA.y-posB.y,2))
                
            else:
                raise TypeError("posB is not an instance of Vector2 or tuple")
        else:
            raise TypeError("posA is not an instance of Vector2 or tuple")
    def tuple(self):
        return (self.x,self.y)
    def multiplyVectors(vectorA, vectorB):
        if isinstance(vectorA, Vector2) or isinstance(vectorA, tuple):
            if isinstance(vectorB, Vector2) or isinstance(vectorB, tuple):
                if type(vectorA) == tuple:
                    vectorA = Vector2(vectorA[0], vectorA[1])
                if type(vectorB) == tuple:
                    vectorB = Vector2(vectorB[0], vectorB[1])
                return Vector2(vectorA.x*vectorB.x,vectorA.y*vectorB.y)
                
            else:
                raise TypeError("vectorB is not an instance of Vector2 or tuple")
        else:
            raise TypeError("vectorA is not an instance of Vector2 or tuple")
    def addVectors(vectorA, vectorB):
        if isinstance(vectorA, Vector2) or isinstance(vectorA, tuple):
            if isinstance(vectorB, Vector2) or isinstance(vectorB, tuple):
                if type(vectorA) == tuple:
                    vectorA = Vector2(vectorA[0], vectorA[1])
                if type(vectorB) == tuple:
                    vectorB = Vector2(vectorB[0], vectorB[1])
                return Vector2(vectorA.x+vectorB.x,vectorA.y+vectorB.y)
                
            else:
                raise TypeError("vectorB is not an instance of Vector2 or tuple")
        else:
            raise TypeError("vectorA is not an instance of Vector2 or tuple")
    def subtractVectors(vectorA, vectorB):
        if isinstance(vectorA, Vector2) or isinstance(vectorA, tuple):
            if isinstance(vectorB, Vector2) or isinstance(vectorB, tuple):
                if type(vectorA) == tuple:
                    vectorA = Vector2(vectorA[0], vectorA[1])
                if type(vectorB) == tuple:
                    vectorB = Vector2(vectorB[0], vectorB[1])
                return Vector2(vectorA.x-vectorB.x,vectorA.y-vectorB.y)
                
            else:
                raise TypeError("vectorB is not an instance of Vector2 or tuple")
        else:
            raise TypeError("vectorA is not an instance of Vector2 or tuple")
    def divideVectors(vectorA, vectorB):
        if isinstance(vectorA, Vector2) or isinstance(vectorA, tuple):
            if isinstance(vectorB, Vector2) or isinstance(vectorB, tuple):
                if type(vectorA) == tuple:
                    vectorA = Vector2(vectorA[0], vectorA[1])
                if type(vectorB) == tuple:
                    vectorB = Vector2(vectorB[0], vectorB[1])
                return Vector2(vectorA.x/vectorB.x,vectorA.y/vectorB.y)
                
            else:
                raise TypeError("vectorB is not an instance of Vector2 or tuple")
        else:
            raise TypeError("vectorA is not an instance of Vector2 or tuple")
    def compareVectors(vectorA, vectorB):
        if isinstance(vectorA, Vector2) or isinstance(vectorA, tuple):
            if isinstance(vectorB, Vector2) or isinstance(vectorB, tuple):
                if isinstance(vectorA, Vector2):
                    vectorA = vectorA.tuple()
                if isinstance(vectorB, Vector2):
                    vectorB = vectorB.tuple()
                return vectorA == vectorB
            else:
                raise TypeError("vectorB is not an instance of Vector2 or tuple")
        else:
            raise TypeError("vectorA is not an instance of Vector2 or tuple")
    
    def raycast(start, distance:int, direction:float, scene: Scene, stop=False) -> list:
        if isinstance(start, Vector2) or isinstance(start, tuple):
            if isinstance(distance, float) or isinstance(distance, int):
                if isinstance(direction, float) or isinstance(direction, int):
                    collisions = []
                    x=math.sin(direction)
                    y=math.cos(direction)
                    end = False
                    for i in range(distance):
                        hbox = Hitbox().Rect(i*x,i*y,1,1)
                        collided = False
                        for item in scene.getObjects().GetList():
                            if not end:
                                if item.hitbox != None:
                                    if hbox.checkCollision(item.hitbox):
                                        collision = item
                                        collided = True
                                        if stop:
                                            end = True
                        if collided:
                            collisions.append((collision,Vector2(i*x,i*y)))
                    return collisions
                else:
                    raise TypeError("direction needs to be an int or float")
            else:
                raise TypeError("distance needs to be an int or float")
        else:
            raise TypeError("start is not an instance of Vector2 or tuple")
    
    def directionFrom(vectorA, vectorB):
        if isinstance(vectorA, Vector2) or isinstance(vectorA, tuple):
            if isinstance(vectorB, Vector2) or isinstance(vectorB, tuple):
                if type(vectorA) == tuple:
                    vectorA = Vector2(vectorA[0], vectorA[1])
                if type(vectorB) == tuple:
                    vectorB = Vector2(vectorB[0], vectorB[1])

                return math.atan2(vectorA.x-vectorB.x, vectorA.y-vectorB.y)/math.pi*180
                
            else:
                raise TypeError("vectorB is not an instance of Vector2 or tuple")
        else:
            raise TypeError("vectorA is not an instance of Vector2 or tuple")

class Physics():
    def __init__(self, gameObject, mass=10, static=False):
        self.vel = [0,0]
        self.mass = mass
        self.gameObject = gameObject
        self.force = self.mass * 10
        self.static = static
    def Update(self):
        
        if not self.static:
            self.force = self.mass * 10
            self.vel[1] += 0.5

            #limit movement
            self.vel[0] /= 1+(0.03/(self.gameObject.tfg.deltaTime*60))
            self.vel[1] /= 1+(0.03/(self.gameObject.tfg.deltaTime*60))

            self.gameObject.changePosition(x=self.vel[0]*self.gameObject.tfg.deltaTime*60, y=self.vel[1]*self.gameObject.tfg.deltaTime*60)
            collided = False
            for item in self.gameObject.scene.getObjects().GetList():
                if item != self.gameObject and item.hitbox != None:
                    if item.hitbox.checkCollision(self.gameObject.hitbox):
                        collision = item.hitbox
                        collided = True
                        break
            if collided:
                collisionPoint = Hitbox.getCollisionPoint(self.gameObject.hitbox, collision, 2)
                while self.gameObject.hitbox.checkCollision(collision):
                    self.gameObject.changePosition(x=-(self.vel[0]/10), y=-(self.vel[1]/10))
                    #print(self.gameObject.pos, [self.gameObject.hitbox.x, self.gameObject.hitbox.y])#-(self.vel[0]/10),-(self.vel[1]/10))
                #print(self.vel[1],collisionPoint.x-self.gameObject.pos[0],self.gameObject.pos[3])
                
                #if collisionPoint.x-self.gameObject.pos[0] > self.gameObject.pos[3]/2:
                #    self.addForce(x=((self.vel[1]+0.1)*4), y=self.vel[1]/20)#-((collisionPoint.x-self.gameObject.pos[0])/5))
                
                #if collisionPoint.x-self.gameObject.pos[0] < self.gameObject.pos[3]/2:
                #    self.addForce(x=-((self.vel[1]+0.1)*4), y=self.vel[1]/20)
                
                self.gameObject.changePosition(x=(self.vel[0]/10)*self.gameObject.tfg.deltaTime*60, y=(self.vel[1]/10)*self.gameObject.tfg.deltaTime*60)
                self.vel = [-self.vel[0]/2,-self.vel[1]/2]
            
        return self
    def addForce(self, x=0, y=0):
        self.vel[0] += x
        self.vel[1] += y
        return self


class Object:
    def __init__(self, window, name, pos: tuple, hitbox=None, physics=None):
        self.name = name
        self.pos = pos
        self.hitbox = hitbox
        self.window = window
        self.rendered = False
        self.scene = None

        
    def setPosition(self, x=None, y=None, z=None):

        if x == None:
            x = self.pos[0]
        if y == None:
            y = self.pos[1]
        if z == None:
            z = self.pos[2]

        self.pos = (x,y,z)
        return self

    def getPosition(self):
        return self.pos

    def getName(self):
        return self.name

    def getHitbox(self):
        return self.hitbox

    #slef
    def getWindow(slef):
        return(slef.window);

    def changePosition(self, x=None, y=None, z=None):

        if x == None:
            x = 0
        if y == None:
            y = 0
        if z == None:
            z = 0

        self.pos = (self.pos[0]+x,self.pos[1]+y,self.pos[2]+z)
        self.hitbox.x = self.pos[0]-self.tfg.mainCamera.pos.x
        self.hitbox.y = self.pos[1]-self.tfg.mainCamera.pos.y
        return self

    def render(slef):
        pass

class ObjectList:
    def __init__(self, lis):
        if isinstance(lis, list):
            pass
        else:
            raise TypeError(f"{object} {type(object)} is not an instance of list")
            return False
        
        self.list_ = lis

    def FindByName(self, name: str):
        for i in self.list_:
            if i.name == name:
                return i
        raise Exception(f"""No object in named {name}
possible solution: did you add it to the scene?""")
        return False
    
    def GetList(self):
        return self.list_
    
class Text(Object):
    def __init__(self, tfg, name, pos: tuple, text, size, color="black", hitbox=None, physics=None, ui=False):
        if physics == None:
            self.physics = Physics(self, static=True)
        else:
            self.physics = physics
        Object.__init__(self, tfg.window, name, pos, hitbox, self.physics)
        self.text = text
        self.tfg = tfg
        self.textSize = size
        self.color = color
        self.ui = ui
    
    def render(self):
        if self.ui:
            self.tfg.canvas.create_text(self.pos[0], self.pos[1], text=self.text, anchor="nw", fill=self.color, font=(f'Helvetica {self.textSize}'))
        else:
            self.tfg.canvas.create_text(self.pos[0]-self.tfg.mainCamera.pos.x, self.pos[1]-self.tfg.mainCamera.pos.y, text=self.text, anchor="nw", fill=self.color, font=(f'Helvetica {self.textSize}'))
        if self.hitbox != None:
            self.hitbox.x = self.pos[0]-self.tfg.mainCamera.pos.x
            self.hitbox.y = self.pos[1]-self.tfg.mainCamera.pos.y


class Rect(Object):
    def __init__(self, tfg, name, pos: tuple, color, outline="", hitbox=None, physics=None, ui=False):
        if physics == None:
            self.physics = Physics(self, static=True)
        else:
            self.physics = physics
        Object.__init__(self, tfg.window, name, pos, hitbox, self.physics)
        self.color = color
        self.tfg = tfg
        self.outline = outline
        self.ui = ui
        self.pos = pos
    
    def setPosition(self, x=None, y=None, width=None, height=None):
        if x == None:
            x = self.pos[0]
        if y == None:
            y = self.pos[1]
        if width == None:
            width = self.pos[2]
        if height == None:
            height = self.pos[3]

        self.pos = (x, y, width, height)
    
    def changePosition(self, x=0, y=0, width=0, height=0):
        self.pos = (self.pos[0]+x,self.pos[1]+y,self.pos[2]+width,self.pos[3]+height)
        if self.hitbox != None:
            self.hitbox.x = self.pos[0]-self.tfg.mainCamera.pos.x
            self.hitbox.y = self.pos[1]-self.tfg.mainCamera.pos.y
        return self
    
    def getPosition(self):
        return self.pos
    
    def render(self):
        self.physics.Update()
        if self.ui:
            self.tfg.canvas.create_rectangle(self.pos[0], self.pos[1], self.pos[0]+self.pos[2], self.pos[1]+self.pos[3], fill=self.color, outline=self.outline)

        else:
            self.tfg.canvas.create_rectangle(self.pos[0]-self.tfg.mainCamera.pos.x, self.pos[1]-self.tfg.mainCamera.pos.y, self.pos[0]-self.tfg.mainCamera.pos.x+self.pos[2], self.pos[1]-self.tfg.mainCamera.pos.y+self.pos[3], fill=self.color, outline=self.outline)
        if self.hitbox != None:
            self.hitbox.x = self.pos[0]-self.tfg.mainCamera.pos.x
            self.hitbox.y = self.pos[1]-self.tfg.mainCamera.pos.y

class Camera(Object):
    def __init__(self, tfg, pos):

        Object.__init__(self, tfg.window, "Main Camera", pos, None, Physics(self, static=True))
        self.tfg = tfg
    
    def render(self):
        pass

    def setPosition(self, x=None, y=None):

        if x == None:
            x = self.pos.x
        if y == None:
            y = self.pos.y
    
    def changePosition(self, x=None, y=None, z=None):

        if x == None:
            x = 0
        if y == None:
            y = 0

        self.pos = Vector2(self.pos.x+x,self.pos.y+y)
        return self

class Image(Object):
    def __init__(self, tfg, name, pos, imgPath, hitbox=None, physics=None, ui=False):
        if physics == None:
            self.physics = Physics(self, static=True)
        else:
            self.physics = physics
        Object.__init__(self, tfg.window, name, pos, hitbox, self.physics)
        self.imgPath = imgPath
        self.tfg = tfg
        self.img2 = PILImage.open(self.imgPath)
        self.img = ImageTk.PhotoImage(self.img2)
        self.ui = ui

        #img = ImageTk.PhotoImage(PILImage.open(imgPath))
        #tfg.tkinter.Label(tfg.window,image=img).pack()#.grid(column=0, row=0)#place(relx=self.pos[0], rely=self.pos[1], anchor = 'nw')

    def resize(self, width, height):
        self.img2 = self.img2.resize((width,height), PILImage.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img2)

    def render(self):
        #self.image = self.tfg.tkinter.Label(self.tfg.window,image=self.img).place(relx=self.pos[0], rely=self.pos[1], anchor = 'nw')
        if self.ui:
            self.tfg.canvas.create_image(self.pos[0],self.pos[1],anchor="nw", image=self.img)
            
        else:
            self.tfg.canvas.create_image(self.pos[0]-self.tfg.mainCamera.pos.x,self.pos[1]-self.tfg.mainCamera.pos.y,anchor="nw", image=self.img)
        if self.hitbox != None:
            self.hitbox.x = self.pos[0]-self.tfg.mainCamera.pos.x
            self.hitbox.y = self.pos[1]-self.tfg.mainCamera.pos.y

    def getHeight(self):
        return self.img.height()

    def getWidth(self):
        return self.img.width()


def LoadImage(path):
    return ImageTk.PhotoImage(PILImage.open(path))


class Data:
    def save(key:str, data, overwrite:bool=True, file:str = ".tfgdata"):
        try:
            with open(file, "r") as f:
                pass
        except:
            with open(file, "w") as f:
                pass

        exists = False
        keyIndex = 0

        with open(file, "r") as f:
            saveFile = f.read()
            keyIndex = saveFile.find(key+"\neok\n")
            if keyIndex != -1:
                exists = True

        if exists and not overwrite:
            raise Exception(f"overwrite is set to false but the key exist in the {file} file")

        else:
            if exists:
                i = 0
                comb = ""
                while i < saveFile.find(key+"\neok\n"):
                    comb += saveFile[i]
                    
                    i+=1
                
                i = saveFile.find("\neod\n",keyIndex)+5
                while i < len(saveFile):
                    comb+=saveFile[i]
                    i+=1
                with open(file, "w") as f:
                    f.write(comb)

            with open(file, "a") as f:
                f.write(key+"\neok\n")
                f.write(str(type(data))+"\neot\n")
                f.write(str(data)+"\neod\n")

    def getData(key:str, file:str = ".tfgdata", showDatatypeError:bool = False):
        try:
            with open(file, "r") as f:
                pass
        except:
            with open(file, "w") as f:
                pass

        with open(file, "r") as f:
            saveFile = f.read()
            keyIndex = saveFile.find(key+"\neok\n")
            if keyIndex == -1:
                raise Exception(f"the key '{key}' isn't in the file '{file}'")
            else:
                keyIndex = saveFile.find(key+"\neok\n")
                keyIndex += len(key+"\neok\n")
                i = keyIndex
                datatype = ""
                while i < saveFile.find("\neot\n",keyIndex):
                    datatype += saveFile[i]
                    i+=1
                
                i+=5
                comb = ""

                while i < saveFile.find("\neod\n",keyIndex):
                    comb += saveFile[i]
                    i+=1
                
                if datatype == "<class 'int'>":
                    comb = int(comb)
                elif datatype == "<class 'float'>":
                    comb = float(comb)
                elif datatype != "<class 'str'>":
                    if showDatatypeError:
                        print(f"datatype {datatype} not supported")
                
                return comb