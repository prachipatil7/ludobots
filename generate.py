import pyrosim.pyrosim as pyrosim
import random

def create_world():
    pyrosim.Start_SDF("world.sdf")

    length, width, height = 1, 1, 1
    xpos, ypos, zpos = -3, 3, 0.5
    pyrosim.Send_Cube(name=f"Box", 
                    pos=[xpos, ypos, zpos] , 
                    size=[length, width, height])

    pyrosim.End()

def generate_body():
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

def generate_brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")

    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

    pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
    pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

    for sensor_neuron in [0,1,2]:
        for motor_neuron in [3,4]:
            pyrosim.Send_Synapse( sourceNeuronName = sensor_neuron , 
                                  targetNeuronName = motor_neuron , 
                                  weight = random.uniform(-1,1))

    pyrosim.End()

create_world()
generate_body()
generate_brain()