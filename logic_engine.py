# L07 - Step1.1: Building the Knowledge Base - IT24103439
class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def tell_fact(self, fact_string):
        self.facts.add(fact_string)

    def tell_rule(self, premise_list, conclusion_string):
        self.rules.append((premise_list, conclusion_string))

    def clear_facts(self):
        self.facts.clear()
