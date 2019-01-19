from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from joblib import dump, load
from sklearn import svm
import json
import os

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

decision_tree = DecisionTreeClassifier()
dt_scores = cross_val_score(decision_tree, matches, results, cv=10)
decision_tree = decision_tree.fit(matches_train, results_train)
with open('dt_scores', 'w+') as dt_file:
	dt_file.write("CV Score: %0.2f (+/- %0.2f)" % (dt_scores.mean(), dt_scores.std() * 2))
	dt_file.write("Accuracy: " + str(decision_tree.score(matches_test, results_test)))
dump(decision_tree, 'dt.joblib')
os.system('gsutil cp dt_scores gs://dota2-win-predictor')
os.system('gsutil cp dt.joblib gs://dota2-win-predictor')

random_forest = RandomForestClassifier()
rf_scores = cross_val_score(random_forest, matches, results, cv=10)
random_forest = random_forest.fit(matches_train, results_train)
with open('rf_scores', 'w+') as rf_file:
	rf_file.write("CV Score: %0.2f (+/- %0.2f)" % (rf_scores.mean(), rf_scores.std() * 2))
	rf_file.write("Accuracy: " + str(random_forest.score(matches_test, results_test)))
dump(random_forest, 'rf.joblib')
os.system('gsutil cp rf_scores gs://dota2-win-predictor')
os.system('gsutil cp rf.joblib gs://dota2-win-predictor')

svm = svm.LinearSVC(random_state=0, tol=1e-5)
svm_scores = cross_val_score(svm, matches, results, cv=10)
svm = svm.fit(matches_train, results_train)
with open('svm_scores', 'w+') as svm_file:
	svm_file.write("CV Score: %0.2f (+/- %0.2f)" % (svm_scores.mean(), svm_scores.std() * 2))
	svm_file.write("Accuracy: " + str(svm.score(matches_test, results_test)))
dump(svm, 'svm.joblib')
os.system('gsutil cp svm_scores gs://dota2-win-predictor')
os.system('gsutil cp svm.joblib gs://dota2-win-predictor')

neural_network = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=42)
nn_scores = cross_val_score(neural_network, matches, results, cv=10)
neural_network = neural_network.fit(matches_train, results_train)
with open('nn_scores', 'w+') as nn_file:
	nn_file.write("CV Score: %0.2f (+/- %0.2f)" % (nn_scores.mean(), nn_scores.std() * 2))
	nn_file.write("Accuracy: " + str(neural_network.score(matches_test, results_test)))
dump(neural_network, 'nn.joblib')
os.system('gsutil cp nn_scores gs://dota2-win-predictor')
os.system('gsutil cp nn.joblib gs://dota2-win-predictor')

logistic_regression = LogisticRegression()
lr_scores = cross_val_score(logistic_regression, matches, results, cv=10)
logistic_regression = logistic_regression.fit(matches_train, results_train)
with open('lr_scores', 'w+') as lr_file:
	lr_file.write("CV Score: %0.2f (+/- %0.2f)" % (lr_scores.mean(), lr_scores.std() * 2))
	lr_file.write("Accuracy: " + str(logistic_regression.score(matches_test, results_test)))
dump(logistic_regression, 'lr.joblib')
os.system('gsutil cp lr_scores gs://dota2-win-predictor')
os.system('gsutil cp lr.joblib gs://dota2-win-predictor')
