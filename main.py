#https://owlready2.readthedocs.io/en/v0.37/onto.html
from owlready2 import *
# https://snakes.ibisc.univ-evry.fr/tutorial/first-steps-with-snakes.html
from snakes.nets import *
import snakes.pnml # export in PNML
#draw PN https://snakes.ibisc.univ-evry.fr/API/plugins/gv.html
import snakes.plugins
snakes.plugins.load(['gv','labels'], 'snakes.nets', 'nets') #['gv','hello'] #multiple plugins
from nets import *

#def print_hi(name):

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    onto = get_ontology("C:\python_space\owl2pn\BRCcase1.owl")
    onto.load()
    n = PetriNet('MFnet') # Create PN
    #Pn = 1  # counter to for place names
    #Tn = 1
    irihead = "http://www.zkhoneycomb.com/formats/metagInOwl#"  # prefix of iri

    #Use connect_sysml_InternalBlockDiagram to search starting points of relationships
    # connect_sysml_InternalBlockDiagram
    cr_iri = irihead + 'connect_sysml_InternalBlockDiagram'
    cr_class = onto.search_one(iri=cr_iri)
    cr_inds = cr_class.instances()
    fromrole = [i for i in cr_inds if '_fromrole_' in str(i)] # list of starting roles of relationships
    torole = [i for i in cr_inds if '_torole_' in str(i)]   # list of ending roles of relationships
    existing_ob = []  # stores created objects

    for fr1 in fromrole:
        # fr1 = fromrole[0] #_ac25
        ##create linked Object if not existing
        ob1 = fr1.linkToObject[0]  # the start object of the relationship #_01b3
        ob1_name = ''
        local_labs = []
        for i in range(0, len(ob1.hasProperty)):
            local_labs.append(ob1.hasProperty[i].localLabel[0]) #['type', 'name', 'initial marking', 'variable', 'operation system', 'capability']
        #ob1_name = ob1_name + '_' + ob1.hasProperty[local_labs.index('name')].value[0] + '_' + ob1.hasProperty[local_labs.index('variable')].value[0]
            #ob1_name = ob1_name + '_' + ob1.hasProperty[i].value[0]  # ['coils']
        ob1_name = ob1.hasProperty[local_labs.index('name')].value[0]
        ob1_lab = ob1.hasProperty[local_labs.index('variable')].value[0]
        if not (ob1 in existing_ob):
            ob_class = ob1.is_a[0]  # get class
            if 'object_material' in str(ob_class):  # Material class
                mk = ob1.hasProperty[local_labs.index('initial marking')].value[0] #'initial marking'
                cap = ob1.hasProperty[local_labs.index('capability')].value[0] #'initial marking'
                #inimk = [{ "ini_marking": mk, "capacity": cap}]
                n.add_place(Place(ob1_name, [int(mk), int(cap)]))
                n.place(ob1_name).label(foo=ob1_lab)
                # n.add_place(Place('P'+str(Pn), ob1_name))
                # Pn = Pn+1
            # elif 'object_Connector' in str(ob_class):  # Connector class
            #     n.add_place(Place('P' + ob1_name))
            #     # Pn = Pn+1
            elif 'object_InternalBlock' in str(ob_class):  # physical components class
                #exp = 'firing_time=' + ob1.hasProperty[local_labs.index('firing time')].value[0] + \
                #      ',priority:' + ob1.hasProperty[local_labs.index('priority')].value[0] + \
                #      ',reservation:' + ob1.hasProperty[local_labs.index('reservation')].value[0]
                exp = ob1.hasProperty[local_labs.index('firing time')].value[0]
                n.add_transition(Transition(ob1_name, Expression('t=='+exp)))
                n.transition(ob1_name).label(foo=ob1_lab)
                # Tn = Tn+1
            existing_ob.append(ob1)
        r1 = fr1.linkFromRelationship[0]  ##Find linked relationship #_15ab
        torole1 = [i for i in r1.linkRelationshipAndRole if '_torole_' in str(i)]  # fc93
        match_str = str(torole1[0])[-11:]  # 'torole_fc93'
        tr1 = [i for i in torole if match_str in str(i)][0]
        ob2 = tr1.linkToObject[0]  # the ending object of the relationship #_7b08
        ob2_name = ''
        local_labs = []
        for i in range(0, len(ob2.hasProperty)):
            local_labs.append(ob2.hasProperty[i].localLabel[0])  # ['type', 'name', 'initial marking', 'variable', 'operation system', 'capability']
        #ob2_name = ob2_name + '_' + ob2.hasProperty[local_labs.index('name')].value[0] + '_' + \
        #           ob2.hasProperty[local_labs.index('variable')].value[0]
        ob2_name = ob2.hasProperty[local_labs.index('name')].value[0]
        ob2_lab = ob2.hasProperty[local_labs.index('variable')].value[0]
        if not (ob2 in existing_ob):
            ob_class = ob2.is_a[0]  # get class
            if 'object_material' in str(ob_class):  # Material class
                mk = ob2.hasProperty[local_labs.index('initial marking')].value[0]  # 'initial marking'
                cap = ob2.hasProperty[local_labs.index('capability')].value[0]  # 'initial marking'
                # inimk = [{ "ini_marking": mk, "capacity": cap}]
                n.add_place(Place(ob2_name, [int(mk), int(cap)]))
                n.place(ob2_name).label(foo=ob2_lab)
                n.add_output(ob2_name, ob1_name, Value('move'))
                # Pn = Pn+1
            # elif 'object_Connector' in str(ob_class):  # Connector class
            #     n.add_place(Place('P' + ob2_name))
            #     n.add_output('P' + ob2_name, 'T' + ob1_name, Value('move'))
            #     # Pn = Pn+1
            elif 'object_InternalBlock' in str(ob_class):  # physical components class
                exp = ob2.hasProperty[local_labs.index('firing time')].value[0]
                n.add_transition(Transition(ob2_name, Expression('t==' + exp)))
                n.transition(ob2_name).label(foo=ob2_lab)
                n.add_input(ob1_name, ob2_name, Value('move'))
                # Tn = Tn+1
            existing_ob.append(ob2)
        elif (ob1 in existing_ob) and (ob2 in existing_ob):
            ob_class = ob1.is_a[0]  # get class
            if 'object_InternalBlock' in str(ob_class):  # physical components class
                n.add_output(ob2_name, ob1_name, Value('move'))
            else:
                n.add_input(ob1_name, ob2_name, Value('move'))

    #for engine in ('neato', 'dot', 'circo', 'twopi', 'fdp'):
    for engine in ('neato', 'dot', 'circo', 'twopi', 'fdp'):
        n.draw('test-gv-%s.png' % engine, engine=engine)

    # export in PNML #https://snakes.ibisc.univ-evry.fr/API/pnml.html
    pn1 = dumps(n)
    # write to a txt file
    fpn = open("pn_model.pnml", "wt")
    n = fpn.write(pn1)
    fpn.close()




