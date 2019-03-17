#coral1.py
import maya.cmds as cmds
import functools
import math

def UI(pWindowTitle, makeCoral):
    """
    Creating the user Interface to input various paramters to create a coral fan
    """
    windowID = 'Coral Fan'
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
        
    #UI window  
    cmds.window(windowID, title = pWindowTitle, sizeable=True, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,100), (2,200), (3,200)],
                         columnOffset = [(1,'right', 3)])
    
    #input fields
    cmds.separator(h=10,style='none')
    
    cmds.text(label='# Subdivisions X: ')
    Base_sub_x = cmds.intSlider(min = 3, max = 20, value=3, step=1)
    cmds.separator(h=10,style='none')
    
    cmds.text(label='# Subdivisions Y: ')
    Base_sub_y = cmds.intSlider(min = 3, max = 20, value=3, step=1)
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Center Base Radius: ')
    Base_radius = cmds.floatField()
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Center Base Hieght Factor: ')
    Base_hieght = cmds.intSlider(min = 30, max = 100, value=30, step=1)
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Bottom Base Radius Factor: ')
    Bottom_base_factor_r = cmds.floatField()
    cmds.separator(h=10,style='none') 
    
    cmds.text(label='Bottom Base Height Factor: ')
    Bottom_base_factor_h = cmds.floatField()
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Max Branches: ')
    Max = cmds.intSlider(min = 1, max = 10, value=1, step=1)
    cmds.separator(h=10,style='none')

    cmds.text(label='Branch Angle: ')
    Branch_angle = cmds.intSlider(min = 1, max = 30, value=1, step=1)
    cmds.separator(h=10,style='none') 
    
    cmds.text(label='Branch Height Start Factor: ')
    Branch_start_height_factor = cmds.floatSlider( min=0, max=0.5, value=0, step=0.1 )
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Branch Height Decrease Factor: ')
    Branch_decrease_factor_h = cmds.floatSlider( min=1, max=2, value=1, step=0.1 )
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Branch Radius Decrease Factor: ')
    Branch_decrease_factor_r = cmds.floatSlider( min=1, max=2, value=1, step=0.1 )
    cmds.separator(h=10,style='none') 
    
    cmds.text(label='Include Criss-Cross? ')
    Include_right = cmds.optionMenu( w = 100)
    cmds.menuItem( label='True' )
    cmds.menuItem( label='False' )
    cmds.separator(h=10,style='none') 
   
    
    #apply button calls makeCoral
    cmds.button(label='Apply', command=functools.partial(makeCoral, Base_sub_x, Base_sub_y, Base_radius, Base_hieght, 
                                                            Bottom_base_factor_r, Bottom_base_factor_h, Max, Branch_angle, Include_right, Branch_start_height_factor, Branch_decrease_factor_h, Branch_decrease_factor_r))
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    cmds.button(label='Cancel', command=cancelCallback)
    cmds.showWindow()


def makeCoral(Base_sub_x, Base_sub_y, Base_radius, Base_hieght, Bottom_base_factor_r, Bottom_base_factor_h, Max, Branch_angle, Include_right, Branch_start_height_factor, Branch_decrease_factor_h, Branch_decrease_factor_r, *pArgs):
              
    base_sub_x = cmds.intSlider(Base_sub_x, query=True,value = True)
    base_sub_y = cmds.intSlider(Base_sub_y, query=True,value = True)
    base_radius = cmds.floatField(Base_radius, query=True,value = True)
    base_hieght = cmds.intSlider(Base_hieght, query=True,value = True)
    bottom_base_factor_r = cmds.floatField(Bottom_base_factor_r, query=True,value = True)
    bottom_base_factor_h = cmds.floatField(Bottom_base_factor_h, query=True,value = True)
    max = cmds.intSlider(Max, query=True,value = True)
    branch_angle = cmds.intSlider(Branch_angle, query=True,value = True)
    include_right = cmds.optionMenu(Include_right, query=True,value = True)
    branch_start_height_factor = cmds.floatSlider(Branch_start_height_factor, query=True,value = True)
    branch_decrease_factor_h = cmds.floatSlider(Branch_decrease_factor_h, query=True,value = True)
    branch_decrease_factor_r = cmds.floatSlider(Branch_decrease_factor_r, query=True,value = True)
    
    if include_right == "True":
        include_right = True
    else:
        include_right = False
    
    branch_decrease_factor_r = branch_decrease_factor_r + 2*branch_start_height_factor
    base_hieght = base_radius * base_hieght
    
    
    left_sub_x = base_sub_x
    left_sub_y = base_sub_y
    left_radius = base_radius / branch_decrease_factor_r
    left_hieght = base_hieght / branch_decrease_factor_h
    
    right_sub_x = base_sub_x
    right_sub_y = base_sub_y
    right_radius = base_radius / branch_decrease_factor_r
    right_hieght = base_hieght / branch_decrease_factor_h
    right_branch_angle = 360 - branch_angle
    
    bot_base_sub_x = base_sub_x
    bot_base_sub_y = base_sub_y
    bot_base_radius = base_radius * bottom_base_factor_r
    bot_base_hieght = base_hieght/bottom_base_factor_h
    
    bottom_base = cmds.polyCone(n='bottom_base', sx = bot_base_sub_x, sy=bot_base_sub_y, r = bot_base_radius, h= bot_base_hieght)
    base_inst = cmds.polyCone(n='base', sx = base_sub_x, sy=base_sub_y, r = base_radius, h= base_hieght)
    
    base_move = base_hieght/2
    cmds.move(0, base_move, 0, base_inst[0])
    bottom_base_move = bot_base_hieght/2
    cmds.move(0, bottom_base_move, 0, bottom_base[0])
    
    coral_base = cmds.group(empty = True, name ="Coral Fan")
    cmds.parent(bottom_base, coral_base)
    cmds.parent(base_inst, coral_base)
    
    left_branch(base_hieght, 0, 0, 0, 0, 0, left_hieght, branch_angle, branch_start_height_factor, max, left_sub_x, left_sub_y, left_radius, branch_decrease_factor_r, branch_decrease_factor_h, include_right, coral_base)


def left_branch(base_hieght, previous_angle, previous_rise, previous_slide, r_previous_rise, r_previous_slide, left_hieght, branch_angle, branch_start_height_factor, max, left_sub_x, left_sub_y, left_radius, branch_decrease_factor_r, branch_decrease_factor_h, include_right, coral_base):
    
    if max!=0:
        left_inst = cmds.polyCone(n='left#', sx = left_sub_x, sy=left_sub_y, r = left_radius, h= left_hieght)
        angle = branch_angle + previous_angle
        rise = previous_rise + (base_hieght * branch_start_height_factor * math.cos(math.radians(previous_angle)))
        slide = previous_slide + (math.sin(math.radians(previous_angle))* base_hieght * branch_start_height_factor)
        left_move_y =  rise + left_hieght/2 - ((left_hieght - left_hieght * math.cos(math.radians(angle)))/2)
        left_move_z = slide + left_hieght *  math.sin(math.radians(angle)) * 0.5 
        cmds.move(0, left_move_y, left_move_z, left_inst[0])
        cmds.select( left_inst[0])
        cmds.rotate( str(angle) +'deg', 0, 0, r=True )
        
        previous_rise = rise
        previous_slide = slide
        
        if include_right:
            right_inst = cmds.polyCone(n='right#', sx = left_sub_x, sy=left_sub_y, r = left_radius, h= left_hieght)
            if (branch_angle + previous_angle) <=90: 
                r_angle = 360 - (branch_angle + previous_angle)
            else:
                r_angle = 360 - (branch_angle + previous_angle) + 90
            r_rise = r_previous_rise + (base_hieght * branch_start_height_factor * math.cos(math.radians(previous_angle)))
            r_slide = r_previous_slide + (math.sin(math.radians(previous_angle))* base_hieght * branch_start_height_factor)
            right_move_y =  r_rise + left_hieght/2 - ((left_hieght - left_hieght * math.cos(math.radians(r_angle)))/2)
            right_move_z = r_slide + left_hieght *  math.sin(math.radians(r_angle)) * 0.5 
            cmds.move(0, right_move_y, right_move_z, right_inst[0])
            cmds.select( right_inst[0])
            cmds.rotate( str(r_angle) +'deg', 0, 0, r=True )  
            
            r_previous_rise = r_rise
            r_previous_slide = r_slide
        
    else:
        return None
        
    prev_hieght = left_hieght
    left_radius = left_radius / branch_decrease_factor_r
    left_hieght = left_hieght / branch_decrease_factor_h
    
    left_name = cmds.ls(left_inst[0])
    cmds.polyMirrorFace( left_name[0], a = 2 )
    
    if include_right:
        right_name = cmds.ls(right_inst[0])
        cmds.polyMirrorFace( right_name[0], a = 2 )
    
    branches = cmds.group(empty = True, name ="Branches")
    cmds.parent(left_inst, branches)
    if include_right:
        cmds.parent(right_inst, branches)
        
    cmds.parent(branches, coral_base)
    
    return left_branch(prev_hieght, angle, previous_rise, previous_slide, r_previous_rise, r_previous_slide, left_hieght, branch_angle, branch_start_height_factor, max-1, left_sub_x, left_sub_y, left_radius, branch_decrease_factor_r, branch_decrease_factor_h, include_right, coral_base)

UI('Coral Fan Input', makeCoral)