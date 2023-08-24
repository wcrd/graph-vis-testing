import rdflib
import json

g = rdflib.Graph().parse('./static/match_example.ttl', format='turtle')

# helper function to split URIs
def splitURI(URI):
    return URI.toPython().split('#')

# Expected format for DirectedGraph
# { source: 'target', target: 'pnt_1', type: 'hasPoint', source_type: , target_type: },

# We are only interested in these properties from our match example
# s->p->o ; p = { feeds, isPartOf, hasPoint }

# can just loop through and generate the expected output format
output = []
for pred in ['feeds', 'hasPart', 'hasPoint']:
    subj_objs = list(g.subject_objects(rdflib.Namespace("https://brickschema.org/schema/Brick#")[pred]))
    for (subj, obj) in subj_objs:
        # get classes
        subj_class = list(g.objects(subj, rdflib.RDF.type))[0]
        obj_class = list(g.objects(obj, rdflib.RDF.type))[0]

        output.append({
            "source": splitURI(subj)[1],
            "target": splitURI(obj)[1],
            "type": pred,
            "source_class": splitURI(subj_class)[1],
            "target_class": splitURI(obj_class)[1]
        })

with open("./src/working/data_directedGraph.json", 'w') as f:
    f.write(json.dumps(output))