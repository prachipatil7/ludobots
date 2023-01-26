import numpy as np
import pyrosim.pyrosim as pyrosim
import os


class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3,2) * 2 - 1

    def Evaluate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py")

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        length, width, height = 1, 1, 1
        xpos, ypos, zpos = -3, 3, 0.5
        pyrosim.Send_Cube(name=f"Box", 
                          pos=[xpos, ypos, zpos] , 
                          size=[length, width, height])

        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        cube = [1, 1, 1]
        pyrosim.Send_Cube(name=f"Torso", 
                       pos=[0, 0, 1.5] , 
                        size=cube)

        pyrosim.Send_Joint(name = "Torso_FrontLeg",
                       parent= "Torso" , 
                       child = "FrontLeg" , 
                       type = "revolute", 
                       position = [0.5,0,1])

        pyrosim.Send_Cube(name=f"FrontLeg", 
                pos= [0.5, 0, -0.5], 
                size=cube)

        pyrosim.Send_Joint(name = "Torso_BackLeg",
                   parent= "Torso" , 
                   child = "BackLeg" , 
                   type = "revolute", 
                   position = [-0.5,0,1])

        pyrosim.Send_Cube(name=f"BackLeg", 
            pos= [-0.5, 0, -0.5], 
            size=cube)
    
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        for curr_row in range(3):
            for curr_col in range(2):
                pyrosim.Send_Synapse( sourceNeuronName = curr_row , 
                                      targetNeuronName = curr_col+3 , 
                                      weight = self.weights[curr_row][curr_col])

        pyrosim.End()