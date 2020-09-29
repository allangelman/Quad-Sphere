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
    spherels = cmds.ls('quadSphere*', long=True)
    sphereNumber = len(spherels)/2
    sphereNumberStr = str(sphereNumber)
    sphereName = 'quadSphere' + sphereNumberStr
    cmds.select(sphereName, r=True)
    cmds.setAttr('polySphere' + sphereNumberStr + '.radius', valRadius, **kwargs)  

def sphereSubX(sliderX, *args, **kwargs):
    """
    sliderX: intSliderGrp object holding the cap subdivisions x value
        
    Adjusts the subdivisions x of the cap based on the slider value
    """
    
    capls = cmds.ls('quadSphere*', long=True)
    capName = capls[len(capls)-1][1:12]
    cmds.delete(capName)
    quadedSphere()   
     
def sphereSubY(sliderY, *args, **kwargs):
    """
    sliderY: intSliderGrp object holding the cap subdivisions y value
        
    Adjusts the subdivisions y of the cap based on the slider value
    """
    
    capls = cmds.ls('quadSphere*', long=True)
    capName = capls[len(capls)-1][1:12]
    cmds.delete(capName)
    quadedSphere()

sphereRadius_Slider = cmds.floatSliderGrp(label='Cap Radius', columnAlign= (1,'right'), field=True, min=0.5, max=3, value=0, step=0.1, dc = 'empty')
cmds.floatSliderGrp(sphereRadius_Slider,  e=True, dc = partial(adjustSphereRadius, sphereRadius_Slider))

sphereSubX_Slider = cmds.intSliderGrp(label='Cap Density', columnAlign= (1,'right'), field=True, min=4, max=20, value=4, step=1, dc = 'empty')
cmds.intSliderGrp(sphereSubX_Slider, e=True, dc = partial(sphereSubX, sphereSubX_Slider))

sphereSubY_Slider = cmds.intSliderGrp(label='Cap Sections', columnAlign= (1,'right'), field=True, min=3, max=20, value=3, step=1, dc = 'empty')
cmds.intSliderGrp(sphereSubY_Slider, e=True, dc = partial(sphereSubY, sphereSubY_Slider))

#Button
cmds.button(l = "Create Quaded Sphere",  c = "quadedSphere()")
cmds.separator(h=20)
cmds.showWindow()


def quadedSphere():
    sphereRadius = cmds.floatSliderGrp(sphereRadius_Slider, q=True, value=True)
    sphereSubX = cmds.intSliderGrp(sphereSubX_Slider, q=True, value=True)
    sphereSubY = cmds.intSliderGrp(sphereSubY_Slider, q=True, value=True)
    
    if sphereSubX%2 == 1:
        sphereSubX = sphereSubX + 1
    
    totalEdges = sphereSubX*(2*sphereSubY-1)-1  
        
    startEdgesDelete = totalEdges - ((sphereSubX-1)*2)
    
    sphere = cmds.polySphere(n='quadSphere#', r=sphereRadius, sx=sphereSubX, sy=sphereSubY)
   
    spherels = cmds.ls('quadSphere*', long=True)
    sphereName = spherels[len(spherels)-1][1:12]
    
    edgeDeleteList = []
    
    for edgeNum in range(startEdgesDelete, totalEdges+1, 2): 
        edgeString = sphereName + '.e[' + str(edgeNum) + ']'
        edgeDeleteList.append(edgeString)
    
    print(edgeDeleteList)
    cmds.delete(edgeDeleteList)