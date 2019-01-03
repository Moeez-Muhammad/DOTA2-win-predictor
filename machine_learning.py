from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
import scraper
import json

with open('matches.json', 'r') as matchesfile:
	matches = json.load(matchesfile)
with open('results.json') as resultsfile:
	results = json.load(resultsfile)
print(len(matches), len(results))

matches_train, matches_test, results_train, results_test = train_test_split(matches, results, test_size=0.50)

logistic_regression = LogisticRegression(solver='lbfgs')
logistic_regression = logistic_regression.fit(matches_train, results_train)
print(logistic_regression.score(matches_test, results_test))

random_forest = RandomForestClassifier()
random_forest = random_forest.fit(matches_train, results_train)
print(random_forest.score(matches_test, results_test))

decision_tree = DecisionTreeClassifier()
decision_tree = decision_tree.fit(matches_train, results_train)
print(decision_tree.score(matches_test, results_test))

neural_network = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=42)
neural_network = neural_network.fit(matches_train, results_train)
print(neural_network.score(matches_test, results_test))
