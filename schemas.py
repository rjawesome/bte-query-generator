id_extraction_prompt_old = """Your job is to extract the named things from a query and put them in square brackets.
Named things refer to one biological/chemical thing.
A category of things (such as disease, proteins, etc.) is NOT a Named thing

Example query: What diseases are caused by cyclin dependent kinase 2?
Your response would be the text in quotes: "[cyclin dependent kinase 2]"
Since disease is a broad category, it is NOT counted as a named thing! However, cyclin dependent kinase 2 is a specific entity so it is a named thing.

Another example query: Which diseases are related to cyclin dependent kinase 2 via a protein?
Your response would be the text in quotes: "[cyclin dependent kinase 2]"
Since disease is a broad category, it is NOT counted as a named thing! Since protein is a broad category, it is NOT counted as a named thing! However, cyclin dependent kinase 2 is a specific entity so it is a named thing.

Categories DO NOT count as named things!

Respond in EXACTLY THE FORMAT with the square brackets:
[named thing #1] [named thing #2 IF APPLICABLE]
Again, DO NOT respond with a sentence or question or anything else more than one word, just use that exact format with the square brackets. Your response should be the stuff inside the square brackets.
DO NOT include something if it is a general category and not a specific named thing based on the example queries!!!
"""

id_extraction_prompt = """
Your job is to extract the named things from a query and put them in square brackets.
Named things refer to one biological/chemical thing. 
The following (or synonyms) are NOT named things: proteins, genes, molecules, diseases, drugs, proteins

Example query: What diseases are caused by cyclin dependent kinase 2?
Your response would be the text in quotes: "[cyclin dependent kinase 2]"
Since disease is a broad category, it is NOT counted as a named thing! However, cyclin dependent kinase 2 is a specific entity so it is a named thing.

Another example query: Which diseases are related to cyclin dependent kinase 2 via a protein?
Your response would be the text in quotes: "[cyclin dependent kinase 2]"
Since disease is a broad category, it is NOT counted as a named thing! Since protein is a broad category, it is NOT counted as a named thing! However, cyclin dependent kinase 2 is a specific entity so it is a named thing.

Another example query: Which genes are related to alzheimer's via a drug?
Your response would be the text in quotes: "[alzheimer's]"
Since genes is a broad category, it is NOT counted as a named thing! Since drug is a broad category, it is NOT counted as a named thing! However, alzheimer's is a specific entity so it is a named thing.

The following (or synonyms) are NOT named things: proteins, genes, molecules, diseases, drugs, proteins

USE THE FORMAT BELOW:
[named thing #1] [named thing #2 IF APPLICABLE] ...

Your response should only contain named things! Please list ONLY specific named biological/chemical entities and NOT categories of biological/chemical entities. 

Again, DO NOT respond with a sentence or question or anything else more than one word, just use that exact format with the square brackets. 
DO NOT consider context.
DO NOT include intermediate entities.
"""

json_generation_prompt = """
Your job is to generate JSON based on the query given
List of Categories:
biolink:Disease
biolink:Gene
biolink:SmallMolecule
biolink:Drug
biolink:Protein
biolink:SequenceVariant

List of Predicates:
biolink:causes
biolink:caused_by
biolink:particpates_in
biolink:treats
biolink:treated_by
biolink:contributes_to
biolink:affects
biolink:related_to
biolink:has_phenotype
biolink:occurs_together_in_literature_with
biolink:regulates

A query is in the following JSON format (JSON cannot have trailing commas, so make sure to avoid that)
{
    "message": {
         "query_graph": {
             "nodes": {
                "n1": {
                    "categories": ["entity category"],
                    "ids": ["an id"]
                },
                "n2": {
                   "categories": ["entity category"],
                   "ids": ["an id"]
                }
             },
             "edges": {
                "e1": {
                    "subject": "one of the nodes specified in nodes section",
                    "predicates": ["one of the predicates listed above"],
                    "object": "a different node specified in nodes section"
                }
            }
        }
    }
}
For each node, you may specify one or more IDs OR one or more categories. If you use a category you can just directly put the name of the category (as long as it is from the categories list), but if you want to refer to a specific entity [ie. a specific disease, or a specific gene], then it must be converted to an ID.

For the example, What diseases are caused by cyclin dependent kinase 2?. You would know the ID of cyclin dependent kinase 2 is MESH:D051357 (only because I told you). You would then need to figure out the predicate (type of edge) based on the question, for example in this question it would be “biolink:causes”. Then figure out how to order the nodes, so that the order makes sense (it should be [subject] [predicate] [object]. for example for the question above [some gene] [biolink:causes] [some disease]).

Now you can write it in some json. For the question above here would be the json:
{
    "message": {
        "query_graph": {
            "nodes": {
                "n1": {
                    "ids": ["MESH:D051357"]
                },
                "n2": {
                    "categories": ["biolink:Disease"],
                }
              }
             "edges": {
                "e1": {
                    "subject": "n1",
                    "predicates": ["biolink:causes"],
                    "object": "n2"
                }
           }
        }
    }
}

Additionally, multiple edges can be used if needed for the query. In this case only ONE node needs an ID (as long as all other nodes are directly or indirectly connected to it). For example, for the question Which compounds are related to cyclin dependent kinase 2 via a protein? we could use:
{
    "message": {
        "query_graph": {
            "nodes": {
                "n1": {
                    "ids": ["MESH:D051357"]
                },
                "n2": {
                    "categories": ["biolink:Protein"],
                },
                "n3": {
                    "categories: ["biolink:SmallMolecule"]
                }
            },
            "edges": {
                "e1": {
                    "subject": "n1",
                    "predicates": ["biolink:related_to"],
                    "object": "n2"
                },
                "e2": {
                    "subject": "n2",
                    "predicates": ["biolink:related_to"],
                    "object": "n3"
                }
            }
        }
    }
}

Please add "knowledge_type": "inferred" to the edge ONLY for the following special cases (ensure that it EXACTLY matches these cases) AND when the query has EXACTLY one edge:
1. The subject of the edge is a SmallMolecule or Drug, the predicate is biolink:affects, and the object is a Gene or Protein
2. The subject of the edge is a SmallMolecule or Drug, the predicate is biolink:treats, and the object is a Disease

This is an example of adding "knowledge_type": "inferred"
"e1": {
...
"knowledge_type": "inferred"
}

Also, use the SIMPLEST query possible to answer the question. ONLY answer with the JSON (NO OTHER TEXT)
"""