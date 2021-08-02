# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 00:40:08 2021

@author: 33753
"""
import socket
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

#################UDP SERVER###########################
localIP     = '169.254.109.119' #Indique que tu écoutes tout le monde
localPort   = 20001 #Port d'écoute de ton PC/ Port vers lequel la nucléo va envoyer le msg
bufferSize  = 1024
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")  

while(True):
    # Initialize the list where we're going to put our values
    messageINT =[0,0]
    
    # Configure the plot each time in the loop
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.view_init(elev=20, azim=32)
    
    # listen for incoming datagrams 
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    # Our Data is on binary so fo that we need to do fue changes to make it an int
    messageTXT = message.decode('ascii')
    message2 = messageTXT.split(" ")
    accX = int(message2[0])
    accY = int(message2[1])
    messageINT[0] = accX  
    messageINT[1] = accY
    accY = accY/1000 *3 #Acceleration of X 
    accX = accX/1000 *3 #Acceleration of Y
    
    # Print the IP of the client and the data in a list of INT
    print(messageINT)
    print(clientIP)
    
    # Plot the arrows which tell the direction and the value of Acceleration
    ax.quiver(0, 0, 0, accX, 0, 0, color='r', arrow_length_ratio=0.1, label=r'$\vec{AccX}$')
    ax.quiver(0, 0, 0, 0, accY, 0, color='b', arrow_length_ratio=0.1, label=r'$\vec{AccY}$')
    ax.quiver(0, 0, 0, accX,accY,0 , color='g', arrow_length_ratio=0.1, label=r'$\vec{AccY*accX}$')
    plt.legend()
    ax.set_xlabel(r'$x$', fontsize='large')
    ax.set_ylabel(r'$y$', fontsize='large')
    ax.set_zlabel(r'$z$', fontsize='large')
    plt.show()
    ax.clear() #Clear the plot for next measures
    
    # Save our Data in a file for another treatment or analyze
    f = open("Measures4.txt", "a")
    f.write("%s \n" % messageINT) 
    f.close()