from .modules import *

class ConvertFormats():
    def __init__(self, hImg, wImg):
        self.hImg = hImg
        self.wImg = wImg

    def YoloToXYXY(self, center, box):
            xCenter, yCenter = center
            hBox, wBox = box
            
            x1 = int((xCenter - wBox / 2) * self.wImg)
            x2 = int((xCenter + wBox / 2) * self.wImg)
            y1 = int((yCenter - hBox / 2) * self.hImg)
            y2 = int((yCenter + hBox / 2) * self.hImg)

            return x1, y1, x2, y2
        
    def XYXYToYolo(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        xCenter = ((x1 + x2) / 2) / self.wImg
        yCenter = ((y1 + y2) / 2) / self.hImg
        hBox = (y2 - y1) / self.hImg
        wBox = (x2 - x1) / self.wImg

        return xCenter, yCenter, hBox, wBox


class Box():
    def __init__(self, label, wImg, hImg):
        clNum, xCenter, yCenter, wBox, hBox = label
        self.clNum = int(clNum)
        self.xCenter = xCenter
        self.yCenter = yCenter
        self.hBox = hBox
        self.wBox = wBox
        self.hImg = hImg
        self.wImg = wImg

    @classmethod
    def CreateFromtxt(clc, label, wImg, hImg):
        label = list(map(float, label.strip().split(' ')))

        return clc(label, wImg, hImg)
    
    @classmethod
    def CreateFromScreen(clc, point, wImg, hImg):

        w_b = point[1][0] - point[0][0]
        h_b = point[1][1] - point[0][1]

        x1, y1 = point[0][0], point[0][1]
        x3, y3 = point[1][0], point[1][1]

        x2, y2 = x1 + w_b, y1
        x4, y4 = x1, y1 + h_b

        x1, x2 = min(x1, x2, x3, x4), max(x1, x2, x3, x4)
        y1, y2 = min(y1, y2, y3, y4), max(y1, y2, y3, y4)

        xCenter = ((x1 + x2) / 2) / wImg
        yCenter = ((y1 + y2) / 2) / hImg
        hBox = (y2 - y1) / hImg
        wBox = (x2 - x1) / wImg

        if xCenter > 0 and yCenter > 0 and hBox > 0 and wBox > 0:
            label = [int(0), xCenter, yCenter, wBox, hBox]

            return clc(label, wImg, hImg)
        
        return False

    def DefineClass(self):
        USER_INP = simpledialog.askstring(title="Box", prompt="Class:")
        if USER_INP:
            self.clNum = int(USER_INP)

    def YoloToXYXY(self):
            
            self.x1 = int((self.xCenter - self.wBox / 2) * self.wImg)
            self.x2 = int((self.xCenter + self.wBox / 2) * self.wImg)
            self.y1 = int((self.yCenter - self.hBox / 2) * self.hImg)
            self.y2 = int((self.yCenter + self.hBox / 2) * self.hImg)

            return self.clNum, self.x1, self.y1, self.x2, self.y2
    
    
    def XYXYToYolo(self):

        self.xCenter = ((self.x1 + self.x2) / 2) / self.wImg
        self.yCenter = ((self.y1 + self.y2) / 2) / self.hImg
        self.hBox = (self.y2 - self.y1) / self.hImg
        self.wBox = (self.x2 - self.x1) / self.wImg

        return self.clNum, self.xCenter, self.yCenter, self.hBox, self.wBox
    
  
    def PointInRect(self, point):
        x, y = point[0], point[1]

        if (x > self.x1 and x < self.x2 and
            y > self.y1 and y < self.y2) :
            return True
        else :
            return False
    
    def PointInCircle(self, point, center, radius=10):
        check = False
        if ((point[0] - center[0])**2 + (point[1] - center[1])**2) < radius**2:
            check = True
        
        return check
    
    def PointPositionCheck(self, point, pointMove):
        Moving = False

        if self.PointInRect(point):
            trans_x, trans_y = pointMove[0]-point[0], pointMove[1]-point[1]
            self.xCenter += trans_x / self.wImg
            self.yCenter += trans_y / self.hImg

            self.xCenter = max(self.wBox / 2, min(self.xCenter, 1 - self.wBox / 2))
            self.yCenter = max(self.hBox / 2, min(self.yCenter, 1 - self.hBox / 2))

            point = pointMove
            Moving = True
        
        elif self.PointInCircle(point, (self.x1, self.y1)):
            self.x1, self.y1 = pointMove[0], pointMove[1]
            self.XYXYToYolo()

            point = pointMove
            Moving = True
        
        elif self.PointInCircle(point, (self.x2, self.y2)):
            self.x2, self.y2 = pointMove[0], pointMove[1]
            self.XYXYToYolo()
            
            point = pointMove
            Moving = True
        
        return point, Moving

    def GetResult(self, format='Yolo'):
        if format == 'Yolo':
            return self.clNum, self.xCenter, self.yCenter, self.wBox, self.hBox

class ImagesLabels:
    def __init__(self, path_data, folder_name):

        try:
            os.makedirs(os.path.join(path_data, 'Results', folder_name + '_Final'))
        except:
            pass

        imgPath = glob.glob(os.path.join(path_data, folder_name, '*[!.txt]'))

        self.path_data = path_data
        self.folder_name = folder_name
        self.imgPath = imgPath
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.imgPath):
            return_img = self.imgPath[self.index]
            self.name = Path(return_img).stem

            txt_name = return_img.replace(return_img[-4:], ".txt")

            if os.path.isfile(txt_name):
                return_txt = txt_name
            else:
                return_txt = os.path.join(self.path_data, self.folder_name, self.name + '.txt')
                try:  
                    open(return_txt, 'w')
                except:
                    pass
         
            self.index += 1            
            self.return_txt = return_txt
            self.return_img = return_img
            
            return return_txt, return_img, self.name
        
        else:
            raise StopIteration
    
    def Save(self, boxes):
        with open(self.return_txt, 'w') as file_yolo:
            for index, box in enumerate(boxes):
                yolo_box = box.GetResult()
                
                if index + 1 == len(boxes):
                    file_yolo.write(" ".join([str(coord) if i == 0 else f'{coord:.6f}' for i, coord in enumerate(yolo_box)]))
                else:
                    file_yolo.write(" ".join([str(coord) if i == 0 else f'{coord:.6f}' for i, coord in enumerate(yolo_box)])+ "\n")

        target = os.path.join(self.path_data, 'Results', self.folder_name + '_Final', self.name + '.txt')
        os.rename(self.return_txt, target)
        target = os.path.join(self.path_data, 'Results', self.folder_name + '_Final', self.name + '.jpg')
        os.rename(self.return_img, target)
