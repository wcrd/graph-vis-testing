import rdflib
import json

g = rdflib.Graph().parse('./static/match_example_2.ttl', format='turtle')

# helper function to split URIs
def splitURI(URI):
    return URI.toPython().split('#')

# Expected format for TidyTree
# {
#   name: label,
#   children: [ {name, children:[] }, ... ]
# }

# We are only interested in these properties from our match example
# s->p->o ; p = { feeds, isPartOf, hasPoint }

# Need to start with Target, and work our way through
# target_ent = rdflib.Namespace("https://building.com#")['target']
target_ent = rdflib.Namespace("https://building.com#")['eqp_Ahn2Gue3']


# loop
# def get_children(forEnt):
#     children = []

#     for pred in ['feeds', 'hasPart', 'hasPoint']:
#         children_ent = list(g.objects(forEnt, rdflib.Namespace("https://brickschema.org/schema/Brick#")[pred]))
    
#         for ent in children_ent:
#             classType = 'point' if pred=='hasPoint' else 'entity'
#             children.append({ 'uri': ent, 'name': splitURI(ent)[1], 'type': classType, 'rel': pred, 'children': []})
    
#     for child in children:
#         child['children'] = get_children(child['uri'])
    
#     return children

def get_children(forEnt):
    children = []

    for pred in ['feeds', 'hasPart', 'hasPoint']:
        children_ent = list(g.objects(forEnt, rdflib.Namespace("https://brickschema.org/schema/Brick#")[pred]))
    
        for ent in children_ent:
            classType = 'point' if pred=='hasPoint' else 'entity'
            children.append({ 'uri': ent, 'name': splitURI(ent)[1], 'type': classType, 'rel': pred, 'children': get_children(ent)})
    
    
    return children

output = {
    'name': splitURI(target_ent)[1],
    'type': 'entity',
    'children': get_children(target_ent)
}


with open("./src/working/data_TidyTree.json", 'w') as f:
    f.write(json.dumps(output, indent=4))