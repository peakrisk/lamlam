PechaKucha
==========

20 images, 20 seconds for each image.

see:
    random

see:
    time    

::
    
    self.images = []
    self.image = 0
    self.time = 20
    self.number = 20

random
------

Create a random PechaKucha using the images available.

code:

     while self.image < 20:
         yield self.images[random.randint(len(self.images)]
         
         self.image += 1
         

add image
---------

Add an image to the set to choose from

code:

    self.images.append(image)


run
---

Run the show.

code:

     while self.image < self.number
         yield self.images[self.image]

         self.image += 1


start
-----

Go back to the start.

code:

    self.image = 0

     
