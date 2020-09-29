from functools import partial

#Window
cmds.window("Quaded Sphere V.01", sizeable=True, resizeToFitChildren=True) 
cmds.columnLayout( adjustableColumn=True )                                             

#Text 
cmds.separator(h=20)
cmds.text("Adjust Parameters of the Quaded Sphere")
cmds.separator(h=20)

#Cap Funcations
def adjustSphereRadius(sliderRadius, *args, **kwargs):
    """
    sliderRadius: floatSliderGrp object holding the sphere radius value
        
    Adjusts the quaded sphere radius based on the slider value
    """
    
    valRadius = cmds.floatSliderGrp(sliderRadius, q=True, value=True)
    sphereNumberStr = getSphereNumStr()
    cmds.setAttr('polySphere' + sphereNumberStr + '.radius', valRadius, **kwargs)  

def sphereSubX(sliderX, *args, **kwargs):
    """
    sliderX: intSliderGrp object holding the sphere subdivisions x value
        
    Adjusts the subdivisions x of the sphere based on the slider value
    """
    
    sphereName = getSphereName()
    cmds.delete(sphereName)
    quadedSphere()

    #valSliderX = cmds.intSliderGrp(sliderX, q=True, value=True)
    #sphereNumberStr = getSphereNumStr()
    #cmds.setAttr('polySphere' + sphereNumberStr + '.subdivisionsAxis', valSliderX, **kwargs)  
     
def sphereSubY(sliderY, *args, **kwargs):
    """
    sliderY: intSliderGrp object holding the sphere subdivisions y value
        
    Adjusts the subdivisions y of the sphere based on the slider value
    """
    
    sphereName = getSphereName()
    cmds.delete(sphereName)
    quadedSphere()
    
    #valSliderY = cmds.intSliderGrp(sliderY, q=True, value=True)
    #sphereNumberStr = getSphereNumStr()
    #cmds.setAttr('polySphere' + sphereNumberStr + '.subdivisionsHeight', valSliderY, **kwargs)  

sphereRadius_Slider = cmds.floatSliderGrp(label='Sphere Radius', columnAlign= (1,'right'), field=True, min=0.5, max=3, value=0, step=0.1, dc = 'empty')
cmds.floatSliderGrp(sphereRadius_Slider,  e=True, dc = partial(adjustSphereRadius, sphereRadius_Slider))

sphereSubX_Slider = cmds.intSliderGrp(label='Sphere Subdivision Axis', columnAlign= (1,'right'), field=True, min=4, max=20, value=4, step=1, dc = 'empty')
cmds.intSliderGrp(sphereSubX_Slider, e=True, dc = partial(sphereSubX, sphereSubX_Slider))

sphereSubY_Slider = cmds.intSliderGrp(label='Sphere Subdivision Height', columnAlign= (1,'right'), field=True, min=3, max=20, value=3, step=1, dc = 'empty')
cmds.intSliderGrp(sphereSubY_Slider, e=True, dc = partial(sphereSubY, sphereSubY_Slider))

#Button
cmds.button(l = "Create Quaded Sphere",  c = "quadedSphere()")
cmds.separator(h=20)
cmds.showWindow()


def quadedSphere():
    sphereRadius = cmds.floatSliderGrp(sphereRadius_Slider, q=True, value=True)
    sphereSubX = cmds.intSliderGrp(sphereSubX_Slider, q=True, value=True)
    sphereSubY = cmds.intSliderGrp(sphereSubY_Slider, q=True, value=True)
    
    #forcing capSubX to always be even because polySpheres with an odd # of SubdivisionsX can't be quaded with this method of deleting edges
    if sphereSubX%2 == 1:
        sphereSubX = sphereSubX + 1
    
    #calculating the start and end edges to delete
    totalEdges = sphereSubX*(2*sphereSubY-1)-1  
    startEdgesDelete = totalEdges - ((sphereSubX-1)*2)
    
    #creating sphere
    sphere = cmds.polySphere(n='quadSphere#', r=sphereRadius, sx=sphereSubX, sy=sphereSubY)
    sphereName = getSphereName()
    
    #iterating over the edges to delete and filling the edgeDeleteList
    edgeDeleteList = []
    for edgeNum in range(startEdgesDelete, totalEdges+1, 2): 
        edgeString = sphereName + '.e[' + str(edgeNum) + ']'
        edgeDeleteList.append(edgeString)
    cmds.delete(edgeDeleteList)
    
def getSphereName():
    spherels = cmds.ls('quadSphere*', long=True)
    sphereNumber = len(spherels)/2
    sphereNumberStr = str(sphereNumber)
    sphereName = 'quadSphere' + sphereNumberStr
    
    return sphereName
    
def getSphereNumStr():
    spherels = cmds.ls('quadSphere*', long=True)
    sphereNumber = len(spherels)/2
    sphereNumberStr = str(sphereNumber)
    
    return sphereNumberStr
    