# Author: Deena Awny
# Version: 20.03.2020
#TODO

import simplenlg.lexicon as lexicon
import simplenlg.framework as framework
import simplenlg.realiser.english as english
class SimpleNLG:

  def realiseSentence(self, subject, verb, object):
    l = lexicon.Lexicon.getDefaultLexicon()
    nlg = framework.NLGFactory(l)
    r = english.Realiser(l)
    p = nlg.createClause()
    p.setSubject(subject)
    p.setVerb(verb)
    p.setObject(object)
    return r.realiseSentence(p)

# Example 1
nlg = SimpleNLG()
print(nlg.realiseSentence("Girl", "prevented", "officials"))

# References
# [1] SimpleNLG, computer software, downloaded 20 March 2020,
# <https://pypi.org/project/py-rouge/>.

# Important Information
# ----------------------
# Natural Language Generation from Predicates
# Simple nlg tutorial - http://www.ling.helsinki.fi/kit/2008s/clt310gen/docs/simplenlg-tutorial-v37.pdf
# Are there better NLG frameworks ? -> future research/implementation

