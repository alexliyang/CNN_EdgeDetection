import numpy as np
from scipy.misc import imshow
import os
import glob
import cv2
import sys

gene=np.array([-0.5, -1, -1, -1, -1, 8, -1, -1, -1, -1, 0, 0, 0, 0, 2, 0, 0, 0, 0])

class ChuaNetwork(object):
  ''' A software implementation of a cellular neural network invented by Leon Chua.

      Args:
           gene: a vector with 19 elements, starting with the Z value, then the B
                 filter, then the A filter. 
           image_sz: the desired image size, or size to reshape images to
           input_ims: A 4-dimensional matrix containing the images in the form
                      NHWC. 
           image_dir: If a directory containing images is given, the program will 
                      read images from the directory and load them in NHWC format. '''             

  def __init__(self,
               gene,
               image_sz,
               input_ims=None,  
               image_dir=None):
    
    self.gene=gene
    self.directory=image_dir
    self.ims=input_ims
    self.reshape=image_sz
    self.num_channels=1
    self.read_ims
    self.network
    self.Z=self.gene[0]
    self.B=self.gene[1:10].reshape([3, 3])
    self.A=self.gene[10:].reshape([3, 3])



  def read_ims(self):
    ''' Reads images from a folder, converts to grayscale, and compiles them into a single
        matrix in NHWC format. '''
    
    if self.directory!=None and self.ims!=None:
      raise ValueError('both image folder and image file provided: please provide only one')

    if self.directory is not None:
      num_images=len(glob.glob1(self.directory,'*.jpg'))
      self.images=np.zeros([num_images, self.reshape[0], self.reshape[1], self.num_channels])
      i=0
      for filename in os.listdir(self.directory):
        if filename.endswith('.jpg'):
          im=cv2.cvtColor(cv2.imread(filename), cv2.BGR2GRAY)
          im=cv2.resize(im, (self.reshape[0], self.reshape[1]))
          self.images[i, :, :, :]=im[np.newaxis, :, :, np.newaxis]
          i+=1

    elif self.directory is None:
      if self.ims.shape[3]!=1:
        self.ims=np.mean(self.ims, axis=3)
      self.images=np.zeros([self.ims.shape[0], self.reshape[0], self.reshape[1], self.num_channels])
      for i in range(self.images.shape[0]):
        im=self.ims[i, :, :]
        im=cv2.resize(im, (self.reshape[0], self.reshape[1]))
        self.images[i, :, :, :]=im[np.newaxis, :, :, np.newaxis]

    return self.images


  
  def network(self): 
    for i in range(self.images.shape[0]):
      im=self.images[i, :, :, :].reshape([self.reshape[0], self.reshape[1]])
      im=np.pad(im, ((1, 1), (1, 1)), 'edge')
      im_out=np.zeros(im.shape)
      for iter in range(1):
        for r in range(1, im.shape[0]):
          for c in range(1, im.shape[1]): 
            influence=im[r-1:r+2, c-1:c+2]
            im_out[r, c]=im_out[r, c]+self.Z+np.dot(influence.flatten(), self.B.flatten())
            out=(np.exp(im_out[r, c])-np.exp(-im_out[r, c]))/(np.exp(im_out[r, c])+np.exp(-im_out[r, c]))
            im_out[r, c]=im_out[r, c]+out*self.A[1, 1]
            imshow(im_out)
            

data=np.load('cifar.npy')

CNN=ChuaNetwork(gene=gene, image_sz=[80, 80], input_ims=data)
CNN.read_ims()
CNN.network()
