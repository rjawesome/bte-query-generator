# BTE Query Generator using GPT
- Generates BTE queries from a question using GPT
- See notebook for a better explanation of code, or use deployed website to try it out: https://example.com
- Needs a lot more testing
- Currently only supports the following categories
```
List of Categories:
biolink:Disease
biolink:Gene
biolink:SmallMolecule
biolink:Drug
biolink:Protein
biolink:SequenceVariant
```
- Currently only supports the following predicates
```
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
```