import math
import numpy as np
class resample:

    def resize(self, image, scalex , scaley , interpolation ):
        """calls the appropriate funciton to resample an image based on the interpolation method
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        interpolation: method used for interpolation ('either bilinear or nearest_neighbor)
        returns a resized image based on the interpolation method
        """

        if interpolation == 'bilinear':
            return self.Bilinear(image, scalex, scaley)

        elif interpolation == 'nearest_neighbor':
            return self.NearestNeighbor(image, scalex, scaley)

        elif interpolation == "cubic":
            return self.Cubic(image, scalex, scaley)


    # def nearest_neighbor(self, image, scalex, scaley):
    #     """resizes an image using bilinear interpolation approximation for resampling
    #     image: the image to be resampled
    #     fx: scale along x direction (eg. 0.5, 1.5, 2.5)
    #     fx: scale along y direction (eg. 0.5, 1.5, 2.5)
    #     returns a resized image based on the nearest neighbor interpolation method
    #     """
    #
    #     #Write your code for nearest neighbor interpolation here
    #     #img = cv2.imread(image)     shouldn't need to read this here
    #     #res = cv2.resize(img, fx=scalex, fy=scaley, interpolation=cv2.INTER_NEAREST)
    #     res  =  self.NearestNeighbor(image,scalex,scaley) #was nearest_neighbor
    #
    #     return res


    # def bilinear_interpolation(self, image, scalex, scaley):
    #     """resizes an image using bilinear interpolation approximation for resampling
    #     image: the image to be resampled
    #     fx: scale along x direction (eg. 0.5, 1.5, 2.5)
    #     fx: scale along y direction (eg. 0.5, 1.5, 2.5)
    #     returns a resized image based on the bilinear interpolation method
    #     """
    #
    #     # Write your code for bilinear interpolation here
    #
    #     (ow,oh) = image.shape # stores the old image width and height, BE SURE THAT OW AND OH ARE IN THE CORRECT ORDER!!
    #     (nw,nh) = (math.floor(scalex*ow),math.floor(scaley*oh)) # new width and height,again check the (ow,oh) order
    #     new_img = np.zeros(nw,nh) #create matrix populated with zeros,check (ow,oh)
    #     for(i,j) in new_img:
    #         ti = i/nw
    #         tj = j/nh
    #         old_i = math.floor(ti*ow) #the "old image" i coordinate
    #         old_j = math.floor(tj*oh)
    #         tl = image[old_i,old_j] # the top left coordinate
    #         tr = image[old_i+1, old_j] # top right
    #         bl = image[old_i, old_j+1] # bottom left coordinate THINK THIS MAY BE [OLD_I+1,OLD_J]
    #         br = image[old_i+1, old_j+1] # bottom right
    #         ui = ti*ow-old_i #may be ti*oh-old_j
    #         uj = tj*oh-old_j #see ui comment
    #         res = self.bilinear_interpolation(tl,tr,bl,br,(ui,uj))
    #
    #     return res




    def NearestNeighbor(self,image, xScale, yScale):
        """Call to perform nearest neighbor interpolation on an image."""
        (h, w) = image.shape
        newxscale = float(xScale)
        newyscale = float(yScale)
        newHeight = h * newyscale
        newWidth = w * newxscale
        newImage = np.zeros((int(newHeight), int(newWidth)), np.uint8)

        heightRatio = h / newImage.shape[0]
        widthRatio = w / newImage.shape[1]

        for i in range(newImage.shape[0]):
            for j in range(newImage.shape[1]):
                mappedY = round(heightRatio * i, None)
                mappedX = round(widthRatio * j, None)

                if (mappedY == h):
                    mappedY = h - 1
                if (mappedX == w):
                    mappedX = w - 1
                # print("i: ", i, "  j: ",j, "   Mapped i: ", mappedY, "  Mapped j:", mappedX)
                newImage[i, j] = image[mappedY, mappedX] # this was self.image in the github code

        print("finished nn")

        # img = Image.fromarray(newImage)  # CONVERT NUMPY ARRAY TO IMAGE OBJECT
        # tkimage = ImageTk.PhotoImage(img)  # THINK I NEED TO CONVERT rotatedImage TO AN IMAGE OBJECT TO MAKE THIS LINE WORK
        # myvar = Label(self, image=tkimage)
        # myvar.image = tkimage
        # myvar.place(x=700, y=60)
        # cv2.namedWindow("window_name")
        # cv2.imshow("window_name", newImage)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows();

        return newImage

    def linear_interpolation(self, pt1, pt2, unknown):
        """helper function to perform linear interpolation."""
        I1 = float(pt1[1])
        I2 = float(pt2[1])

        x1 = pt1[0]
        x2 = pt2[0]

        x = unknown[0]

        i = (I1 * (x2 - x) / (x2 - x1)) + (I2 * (x - x1) / (x2 - x1))

        return (x, i)

    def bilinear_interpolation(self, pt1, pt2, pt3, pt4, unknown):
        """helper function to perform bilinear interpolation"""
        newPt1 = (pt1[1], pt1[2])
        newPt2 = (pt2[1], pt2[2])
        newPt3 = (pt3[1], pt3[2])
        newPt4 = (pt4[1], pt4[2])

        r1 = self.linear_interpolation(newPt1, newPt2, (unknown[1], unknown[2]))
        r2 = self.linear_interpolation(newPt3, newPt4, (unknown[1], unknown[2]))

        newR1 = (pt1[0], r1[1])
        newR2 = (pt3[0], r2[1])

        p = self.linear_interpolation(newR1, newR2, (unknown[0], unknown[2]))

        return p[1]

    def Bilinear(self,image, xScale, yScale):
        """Call to perform bi-linear interpolation."""
        import math

        (h, w) = image.shape

        newHeight = h * float(yScale)
        newWidth = w * float(xScale)

        hRatio = h / (newHeight + 1)
        wRatio = w / (newWidth + 1)

        newImage = np.zeros((int(newHeight), int(newWidth), 1), np.uint8)

        for i in range(newImage.shape[0]):
            for j in range(newImage.shape[1]):

                y1 = math.floor(hRatio * i)
                y2 = math.ceil(hRatio * i)

                x1 = math.floor(wRatio * j)
                x2 = math.ceil(wRatio * j)

                if (y2 == h):
                    y2 = h - 1
                    y1 = h - 2

                if (x2 == w):
                    x2 = w - 1
                    x1 = w - 2

                if y1 == y2 and x1 == x2:
                    newImage[i, j] = image[y1, x1]
                elif y1 == y2:
                    """"""
                    newImage[i, j] = \
                    self.linear_interpolation((x1, image[y1, x1]), (x2, image[y1, x2]), ((wRatio * j), 0))[1]
                elif x1 == x2:
                    """"""
                    newImage[i, j] = \
                    self.linear_interpolation((y1, image[y1, x1]), (y2, image[y2, x1]), ((hRatio * i), 0))[1]
                else:
                    pt1 = (y1, x1, image[y1, x1])
                    pt2 = (y1, x2, image[y1, x2])
                    pt3 = (y2, x1, image[y2, x1])
                    pt4 = (y2, x2, image[y2, x2])

                    unknown = ((hRatio * i), (wRatio * j), 0)

                    newImage[i, j] = self.bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)

        # output_image_name = "image_name" + "Bilinear" + datetime.now().strftime("%m%d-%H%M%S") + ".jpg"
        # cv2.imwrite(output_image_name, newImage)
        #
        # cv2.namedWindow("window_name")
        # cv2.imshow("window_name", newImage)
        # cv2.waitKey(0)

        return newImage

    def linear_cubic(self, pt1, pt2, pt3, pt4, unknown):
        """helper function for Cubic interpolation"""
        I1 = float(pt1[1])
        I2 = float(pt2[1])
        I3 = float(pt3[1])
        I4 = float(pt4[1])

        x2 = pt2[0]
        x3 = pt3[0]

        x = unknown[0]

        mu = (x - x2) / (x3 - x2)
        mu2 = mu * mu

        a1 = (-0.5 * I1) + (1.5 * I2) - (1.5 * I3) + (0.5 * I4)
        a2 = I1 - 2.5 * I2 + 2 * I3 - 0.5 * I4
        a3 = -0.5 * I1 + 0.5 * I3
        a4 = I2

        i = a1 * mu * mu2 + a2 * mu2 + a3 * mu + a4

        if i > 255:
            i = 255
        if i < 0:
            i = 0

        return (x, i)

    def bi_cubic(self, pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10, pt11, pt12, pt13, pt14, pt15, pt16, unknown,
                 y1, y4):
        """helper function for cubic interpolation"""
        newPt1 = (pt1[1], pt1[2])
        newPt2 = (pt2[1], pt2[2])
        newPt3 = (pt3[1], pt3[2])
        newPt4 = (pt4[1], pt4[2])

        newPt5 = (pt5[1], pt5[2])
        newPt6 = (pt6[1], pt6[2])
        newPt7 = (pt7[1], pt7[2])
        newPt8 = (pt8[1], pt8[2])

        newPt9 = (pt9[1], pt9[2])
        newPt10 = (pt10[1], pt10[2])
        newPt11 = (pt11[1], pt11[2])
        newPt12 = (pt12[1], pt12[2])

        newPt13 = (pt13[1], pt13[2])
        newPt14 = (pt14[1], pt14[2])
        newPt15 = (pt15[1], pt15[2])
        newPt16 = (pt16[1], pt16[2])

        r1 = self.linear_cubic(newPt1, newPt2, newPt3, newPt4, (unknown[1], unknown[2]))
        r2 = self.linear_cubic(newPt5, newPt6, newPt7, newPt8, (unknown[1], unknown[2]))

        r3 = self.linear_cubic(newPt9, newPt10, newPt11, newPt12, (unknown[1], unknown[2]))
        r4 = self.linear_cubic(newPt13, newPt14, newPt15, newPt16, (unknown[1], unknown[2]))

        newR1 = (pt1[0], r1[1])
        newR2 = (pt5[0], r2[1])
        newR3 = (pt9[0], r3[1])
        newR4 = (pt13[0], r4[1])

        # p = self.linear_interpolation(newR1, newR2, (unknown[0], unknown[2]))
        # print("Finding final I")
        p = self.linear_cubic(newR1, newR2, newR3, newR4, (unknown[0], unknown[2]))

        return p[1]

    def Cubic(self, image, xScale, yScale):
        """Call to perform cubic interpolation."""

        (h, w) = image.shape

        newHeight = h * float(yScale)
        newWidth = w * float(xScale)

        hRatio = h / (newHeight + 1)
        wRatio = w / (newWidth + 1)

        newImage = np.zeros((int(newHeight), int(newWidth), 1), np.uint8)

        for i in range(newImage.shape[0]):
            for j in range(newImage.shape[1]):

                x2 = math.floor(wRatio * j)
                x1 = x2 - 1
                x3 = math.ceil(wRatio * j)
                x4 = x3 + 1

                y2 = math.floor(hRatio * i)
                y1 = y2 - 1
                y3 = math.ceil(hRatio * i)
                y4 = y3 + 1

                if x2 == 0:
                    x1 = 0
                if x3 == w - 1 or x3 == w:
                    x3 = w - 1
                    x4 = w - 1

                if y2 == 0:
                    y1 = 0
                if y3 == h - 1 or y3 == w:
                    y3 = h - 1
                    y4 = h - 1

                if x2 == x3 and y2 == y3:
                    newImage[i, j] = image[y2, x2]
                elif y2 == y3:
                    """"""
                    pt1 = (x1, image[y2, x1])
                    pt2 = (x2, image[y2, x2])
                    pt3 = (x3, image[y2, x3])
                    pt4 = (x4, image[y2, x4])
                    unknown = (wRatio * j, 0)
                    newImage[i, j] = self.linear_cubic(pt1, pt2, pt3, pt4, unknown)[1]
                elif x2 == x3:
                    """"""
                    pt1 = (y1, image[y1, x2])
                    pt2 = (y2, image[y2, x2])
                    pt3 = (y3, image[y3, x2])
                    pt4 = (y4, image[y4, x2])
                    unknown = (hRatio * i, 0)
                    newImage[i, j] = self.linear_cubic(pt1, pt2, pt3, pt4, unknown)[1]

                else:
                    """"""
                    pt1 = (y1, x1, image[y1, x1])
                    pt2 = (y1, x2, image[y1, x2])
                    pt3 = (y1, x3, image[y1, x3])
                    pt4 = (y1, x4, image[y1, x4])

                    pt5 = (y2, x1, image[y2, x1])
                    pt6 = (y2, x2, image[y2, x2])
                    pt7 = (y2, x3, image[y2, x3])
                    pt8 = (y2, x4, image[y2, x4])

                    pt9 = (y3, x1,  image[y3, x1])
                    pt10 = (y3, x2, image[y3, x2])
                    pt11 = (y3, x3, image[y3, x3])
                    pt12 = (y3, x4, image[y3, x4])

                    pt13 = (y4, x1, image[y4, x1])
                    pt14 = (y4, x2, image[y4, x2])
                    pt15 = (y4, x3, image[y4, x3])
                    pt16 = (y4, x4, image[y4, x4])

                    unknown = (hRatio * i, wRatio * j, 0)

                    newImage[i, j] = self.bi_cubic(pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10, pt11, pt12, pt13,
                                                   pt14, pt15, pt16, unknown, y1, y4)




        return newImage
