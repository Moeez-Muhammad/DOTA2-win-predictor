from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
import json
import pandas
print("Done importing")

print("Loading matches and results as json...")
with open('matches.json', 'r') as matchesfile:
	matches = json.load(matchesfile)
with open('results.json', 'r') as resultsfile:
	results = json.load(resultsfile)

print("Done")
print(len(matches), len(results))

print("Splitting...")
matches_train, matches_test, results_train, results_test = train_test_split(matches, results, test_size=0.25, shuffle=True)
print(len(matches_train), len(matches_test), len(results_train), len(results_test))

print("DECISION TREE\n-------------------")
decision_tree = DecisionTreeClassifier()
print("Initialized")
print("Fitting...")
decision_tree.fit(matches_train, results_train)
print("Done")
print("Scoring...")
print(decision_tree.score(matches_test, results_test))
print("Creating graph...")
dotfile = open('dtree.dot', 'w')
export_graphviz(decision_tree, out_file=dotfile)

""" random_forest = RandomForestClassifier()
random_forest = random_forest.fit(matches_train, results_train)
print(random_forest.score(matches_test, results_test))

decision_tree = DecisionTreeClassifier()
decision_tree = decision_tree.fit(matches_train, results_train)
print(decision_tree.score(matches_test, results_test))

neural_network = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=42)
neural_network = neural_network.fit(matches_train, results_train)
print(neural_network.score(matches_test, results_test))
 """