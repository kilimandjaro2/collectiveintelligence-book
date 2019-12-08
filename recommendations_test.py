#!/usr/bin/env python3
# encoding: utf-8

# scatterPlots.py	# This file's Name

#from editor import *			# Idea From David Beazley working "en vivo"
								# Toutes les Libraries indispensables
								
# Dans le Terminal: PS1="\$ "     Un prompt minimal!!!

from pprint import pprint		# A importer toujours...car tres utile
# print ("dir() === Indispensables en direct dans le Terminal"); pprint(dir())	


__ref__ = """
# ===  References  ===
# Reworked by ZZ : --- on : --- December 8, 2019 at 16:32:13 EST

LES REFERENCES SONT OBLIGATOIRES...
http://

Created by ZZ - 3/5/18, 7:13 PM.
Copyright (c) 2018 __MyCompanyName__. All rights reserved.

"""

__doc__ = """
# ===  Documentation  ===
# Template  minimum
	  traiter les sources avec ypf
	  https://yapf.now.sh/
(Yet another Python formatter)
# ===========================

=== Procedure a suivre: ===
# <Indispensable>

0/Presentation:
Une seule file qui est auto-suffisante, car elle comporte tout a la fois:
	-Le programme
	-Le lancement de L'Execution
	-Le resultat de l'Execution
tout cela sans quitter notre Editeur favori: BBEDIT!

1/Edition
Pour un maximum de clarte:
	Faire le menage dans les noms de folders et de files (en particulier, des files identiques en .py et .ipynd doivent porter des noms identiques(seule change l'extension)
	
Puis Editer dans BBEDITun job en se servant de ce Template.

2/Runs et Tests
En plus il comporte, via le "if __name__ == '__main__', un moyen de le tester "in extenso" ou de le garder tel quel pour des Imports.

3/Les sorties
Elles sont incorporees a cette file, via un "Cut and paste" dans la variable "output"

4/Une fois totalement edite, la file est incorporee dans Jupyter via un "Cut and paste"

5/Corrections minimes
Apres suppression du "Shebang", ce job runs  directement dans un Notebook sous Jupyter

6/Autre solulion (preferable), l'Import
Il est preferable de faire un import des noms de domaine du fichier  .py, car ainsi on ne conserve qu'un exemplaire de source unique.


Et aussi...

Cas de recuperation d'anciens codes:
====================================
1/3 Examen du contenu:
	deux blancs pour l'indentation ===> 1 tabulation

2/3   2to3 for Converting Python 2 scripts to Python 3
	Ref: la Doc de Python3:
		https://docs.python.org/2/library/2to3.html
		
	explications:
	https://pythonprogramming.net/converting-python2-to-python3-2to3/
	et
	Outil:   2to3 on Line:
	https://www.pythonconverter.com/


3/3	YAPF (Yet another Python formatter)
	https://yapf.now.sh/

"""

import unittest

import recommendations

class DistanceTestCase:

	def testIdentical(self):
		prefs = { 'Nico': {'h': 1, 'b':0.4}, 'Yann': {'h': 1, 'b': 0.4}}
		self.assertEqual(1.0, self.metric(prefs, 'Nico', 'Yann'))

	def testOneEqualElement(self):
		prefs = { 'Nico': {'h': 0.9}, 'Yann': {'h': 0.9}}
		self.assertEqual(1.0, self.metric(prefs, 'Nico', 'Yann'))

	def testEmptyPrefs(self):
		prefs = { 'Nico': {}, 'Yann': {}}
		self.assertEqual(0.0, self.metric(prefs, 'Nico', 'Yann'))

	def testEmptyIntersection(self):
		prefs = { 'Nico': {'h': 1}, 'Yann': {'z': 1}}
		self.assertEqual(0.0, self.metric(prefs, 'Nico', 'Yann'))

	def testAdditionalLeft(self):
		addLeft = self.prefs.copy()
		addLeft['Nico']['c'] = 0.9
		self.assertAlmostEqual(self.metric(self.prefs, 'Nico', 'Yann'),
				self.metric(addLeft, 'Nico', 'Yann'))

	def testAdditionalRight(self):
		addRight = self.prefs.copy()
		addRight['Yann']['c'] = 0.9
		self.assertAlmostEqual(self.metric(self.prefs, 'Nico', 'Yann'),
				self.metric(addRight, 'Nico', 'Yann'))


class SimDistanceTestCase(DistanceTestCase, unittest.TestCase):
	def setUp(self):
		self.metric = recommendations.sim_distance
		self.prefs = { 'Nico': {'h': 0.8, 'b':0.2}, 'Yann': {'h': 0.4, 'b':0.1}}

	def testNormal(self):
# 		self.assertAlmostEqual(0.7080596, self.metric(self.prefs, 'Nico', 'Yann'))		# BUG de Distance Eulerienne corrige
		self.assertAlmostEqual(0.6089710688152306, self.metric(self.prefs, 'Nico', 'Yann'))


class SimPearsonTestCase(DistanceTestCase, unittest.TestCase):
	def setUp(self):
		self.metric = recommendations.sim_pearson
		self.prefs = { 'Nico': {'h': 0.8, 'b':0.2}, 'Yann': {'h': 0.4, 'b':0.1}}

	def testNormal(self):
		self.assertAlmostEqual(1, self.metric(self.prefs, 'Nico', 'Yann'))


class TopMatchesTest(unittest.TestCase):
	def setUp(self):
		self.data = {
				'Nico': { 'Python': 4.5, 'Ruby': 3.0, 'C++': 3.4, 'Java': 2.5 },
				'Yann': { 'Python': 3.0, 'Ruby': 4.5, 'C++': 3.4, 'Java': 1.5 },
				'Josh': { 'Python': 0.5, 'Ruby': 0.0, 'C++': 1.0, 'Java': 5.0 },
				'Kerstin': { 'Chocolate': 5.0 },
				}

	def testBasics(self):
		scores = { 'Yann': 3, 'Kerstin': 2, 'Josh': 1 }
		def stubDistance(prefs, p1, p2):
			self.assertEqual(self.data, prefs)
			if p1 == 'Nico': return scores[p2]
			else: return scores[p1]
		m = recommendations.topMatches(self.data, 'Nico', similarity=stubDistance)
		self.assertEqual([(3, 'Yann'), (2, 'Kerstin'), (1, 'Josh')], m)

	def testNormalWithPearson(self):
		m = recommendations.topMatches(self.data, 'Nico',
				similarity=recommendations.sim_pearson)
		# With pearson, disagreement is worse than no common ground
		self.assertEqual(['Yann', 'Kerstin', 'Josh'], [n for (s,n) in m])

	def testNormalWithDistance(self):
		m = recommendations.topMatches(self.data, 'Nico',
				similarity=recommendations.sim_distance)
		# With distance, disagreement is closer than no common ground
		self.assertEqual(['Yann', 'Josh', 'Kerstin'], [n for (s,n) in m])

	def testNLargetThanCount(self):
		m = recommendations.topMatches(self.data, 'Kerstin', n=2*len(self.data))
		self.assertEqual(len(self.data) - 1, len(m))

class GetRecommendationsTest(unittest.TestCase):
	def setUp(self):
		self.data = {
				'Nico': { 'Python': 4.5, 'Ruby': 3.0, 'C++': 3.4, 'Java': 2.5 },
				'Yann': { 'Python': 3.0, 'Ruby': 4.5, 'C++': 3.4, 'Java': 1.5,
									'Mathematica': 3.5, 'Chocolate': 2.0, 'Patterns': 2.0 },
				'Josh': { 'Python': 0.5, 'Ruby': 0.0, 'C++': 1.0, 'Java': 5.0,
									'Patterns': 5.0 },
				'Kerstin': { 'Python': 0.1, 'Chocolate': 5.0 },
				}

	def testBasics(self):
		r = recommendations.getRecommendations(self.data, 'Nico',
				similarity=recommendations.sim_distance)
		#print recommendations.sim_distance(self.data, 'Nico', 'Yann')
		#print recommendations.sim_distance(self.data, 'Nico', 'Josh')
		#print recommendations.sim_distance(self.data, 'Nico', 'Kerstin')
		#print r
		self.assertEqual(['Mathematica', 'Chocolate', 'Patterns'],
				[n for s,n in r])

class TransformPrefsTest(unittest.TestCase):
	def testBasics(self):
		d = { 'a': {'b': 0.4}, 'c': {'d': 0.5} }
		expected = { 'b': {'a': 0.4}, 'd': {'c' : 0.5} }
		self.assertEqual(expected, recommendations.transformPrefs(d))

	def testEmptyPrefsList(self):
		d = { 'a': {}, 'c': {'d': 0.5} }
		expected = { 'd': {'c' : 0.5} }
		self.assertEqual(expected, recommendations.transformPrefs(d))

	def testOnlyEmptyPrefs(self):
		d = { 'a': {} }
		expected = { }
		self.assertEqual(expected, recommendations.transformPrefs(d))

	def testAllEmpty(self):
		d = { }
		expected = { }
		self.assertEqual(expected, recommendations.transformPrefs(d))

	def testCollect(self):
		d = { 'a': {'z': 0.1}, 'b': {'z' : 0.2}, 'c': {'z': 0.3} }
		expected = { 'z': {'a': 0.1, 'b': 0.2, 'c': 0.3} }
		self.assertEqual(expected, recommendations.transformPrefs(d))


class GetRecommendedItemsTest(unittest.TestCase):
	def testBasics(self):
		d = {'N': {'p': 1.0, 'j': 0.3}, 'Y':{'p': 0.8, 'j': 0.2, 'r':1.0} }
		itemsim = recommendations.calculateSimilarItems(d)
		r = recommendations.getRecommendedItems(d, itemsim, 'N')
		self.assertEqual(1, len(r))
		self.assertEqual('r', r[0][1])
			 

class SimTanimotoTestCase(DistanceTestCase, unittest.TestCase):
	def setUp(self):
		self.metric = recommendations.sim_tanimoto
		self.prefs = { 'Nico': {'h': 0.8, 'b':0.2}, 'Yann': {'h': 0.4, 'b':0.1}}

	def testNormal(self):
		expected = (0.32 + 0.02) / ((0.64 + 0.04) + (0.16 + 0.01) - (0.32 + 0.02))
		self.assertAlmostEqual(expected, self.metric(self.prefs, 'Nico', 'Yann'))


if __name__ == '__main__':
	unittest.main()
