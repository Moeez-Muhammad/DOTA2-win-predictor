from joblib import dump, load
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

dt = load('dt.joblib')
dt_predict = dt.predict(matches_test)
del dt

rf = load('rf.joblib')
rf_predict = rf.predict(matches_test)
del rf

svm = load('svm20.joblib')
svm_predict = svm.predict(matches_test)
del svm

nn = load('nn.joblib')
nn_predict = nn.predict(matches_test)
del nn

lr = load('lr.joblib')
lr_predict = lr.predict(matches_test)
del lr

def compare(list1, list2, results):
	table = [[0, 0], [0, 0]]
	for i in range(list1):
		if list1[i] == list2[i]:
			if list1[i] == results[i]:
				table[0][0] += 1
			else:
				table[1][1] += 1
		else:
			if list1[i] == results[i]:
				table[0][1] += 1
			else:
				table[1][0] += 1
	return table

f = open('mcnemar','w+')
for list1 in [dt_predict, rf_predict, svm_predict, nn_predict, lr_predict]:
	for list2 in [dt_predict, rf_predict, svm_predict, nn_predict, lr_predict]:
		com = compare(list1, list2, results)
		print(com)
		f.write(str(com) + '\n')


