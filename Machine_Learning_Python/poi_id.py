#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Loading the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    
# Data points in the dataset
print "Data points in the dataset:", len(data_dict)

### Removing outliers
data_dict.pop('TOTAL')
data_dict.pop('THE TRAVEL AGENCY IN THE PARK')
data_dict.pop('LOCKHART EUGENE E')

print "Data points after removing outliers:", len(data_dict)

# Number of POI
poi_count=0
npoi_count=0
for name in data_dict:
    if data_dict[name]['poi']==True:
        poi_count+=1
    else:
        npoi_count+=1

print "Number of POI", poi_count
print "Number of non-POI", npoi_count

### Creating new feature(s)

def computeFraction( poi_messages, all_messages ):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
   """

    if poi_messages != 'NaN' and all_messages !='NaN':
        p_messages = float(poi_messages)
        a_messages = float(all_messages)
        fraction = p_messages/a_messages
        return fraction
    else:
        fraction = 0.
        return fraction

# Creating "fraction_from_poi" and "fraction_to_poi" and adding to data_dict
for name in data_dict:
    data_point = data_dict[name]
    from_poi_to_this_person = data_point["from_poi_to_this_person"]
    to_messages = data_point["to_messages"]
    fraction_from_poi = computeFraction( from_poi_to_this_person, to_messages )
    data_dict[name]["fraction_from_poi"] = fraction_from_poi
    
    from_this_person_to_poi = data_point["from_this_person_to_poi"]
    from_messages = data_point["from_messages"]
    fraction_to_poi = computeFraction( from_this_person_to_poi, from_messages )
    data_dict[name]["fraction_to_poi"] = fraction_to_poi
                      

# Initial feature list for selecting the best variables
initial_features_list = ['poi','salary','bonus','to_messages','shared_receipt_with_poi', 'fraction_to_poi',
                 'expenses', 'total_stock_value','total_payments', 'exercised_stock_options', 'restricted_stock',
                'from_messages', 'fraction_from_poi'] 

### Storing to my_dataset for easy export below.
my_dataset = data_dict

### Extracting features and labels from dataset for local testing
data = featureFormat(my_dataset, initial_features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


# Data points to be used in the analysis
print "Data points used in the analysis:", len(features)

 
#Feature Selection - Using SelectKBest to select the variables with higher scores
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.feature_selection import SelectKBest


selector = SelectKBest(f_classif, k = "all")
selector.fit(features, labels)

scores = selector.scores_
index = selector.get_support(True)
print "Features scores:", scores
print "Features index:", index


# Final feature list 
final_features_list = ['poi', 'exercised_stock_options', 'total_stock_value', 'bonus', 'salary' ] 

### Storing to my_dataset for easy export below.
my_dataset = data_dict

### Extracting features and labels from dataset for local testing
data = featureFormat(my_dataset, final_features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Trying a variety of classifiers

# Naive Bayes
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


sss = StratifiedShuffleSplit(labels, n_iter = 1000,test_size = 0.3, random_state=42)
true_negatives = 0
false_negatives = 0
true_positives = 0
false_positives = 0

for train_idx, test_idx in sss:
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_idx:
        features_train.append( features[ii] )
        labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
    # train a classifier
    clf = GaussianNB()
    clf.fit(features_train, labels_train)
    # test the classifier
    pred = clf.predict(features_test)
    for prediction, truth in zip(pred, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1

try:
    total_predictions = true_negatives + false_negatives + false_positives + true_positives
    accuracy = 1.0*(true_positives + true_negatives)/total_predictions
    precision = 1.0*true_positives/(true_positives+false_positives)
    recall = 1.0*true_positives/(true_positives+false_negatives)
    f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
    f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
    print  "Naive Bayes"
    print "accuracy", accuracy
    print "precision",precision
    print "recall",recall
    print "f1",f1
    print "f2",f2
except:
     print "Precision or recall may be undefined due to a lack of true positive predicitons."


# Decision Tree

from sklearn import tree

sss = StratifiedShuffleSplit(labels, n_iter = 1000,test_size = 0.3, random_state=42)
true_negatives = 0
false_negatives = 0
true_positives = 0
false_positives = 0

for train_idx, test_idx in sss:
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_idx:
        features_train.append( features[ii] )
        labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
    # train a classifier
    clf = tree.DecisionTreeClassifier()
    clf.fit(features_train, labels_train)
    # test the classifier
    pred = clf.predict(features_test)
    for prediction, truth in zip(pred, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1
                   
    

try:
    total_predictions = true_negatives + false_negatives + false_positives + true_positives
    accuracy = 1.0*(true_positives + true_negatives)/total_predictions
    precision = 1.0*true_positives/(true_positives+false_positives)
    recall = 1.0*true_positives/(true_positives+false_negatives)
    f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
    f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
    print  "Decision Tree"
    print "accuracy", accuracy
    print "precision",precision
    print "recall",recall
    print "f1",f1
    print "f2",f2
except:
     print "Precision or recall may be undefined due to a lack of true positive predicitons."

# SVM - RBF

from sklearn.svm import SVC

sss = StratifiedShuffleSplit(labels, n_iter = 1000,test_size = 0.3, random_state=42)
true_negatives = 0
false_negatives = 0
true_positives = 0
false_positives = 0

for train_idx, test_idx in sss:
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_idx:
        features_train.append( features[ii] )
        labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
    # train a classifier
    clf = SVC(C=10,kernel="rbf")
    clf.fit(features_train, labels_train)
    # test the classifier
    pred = clf.predict(features_test)
    for prediction, truth in zip(pred, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1
                   
    

try:
    total_predictions = true_negatives + false_negatives + false_positives + true_positives
    accuracy = 1.0*(true_positives + true_negatives)/total_predictions
    precision = 1.0*true_positives/(true_positives+false_positives)
    recall = 1.0*true_positives/(true_positives+false_negatives)
    f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
    f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
    print  "SVM-RBF"
    print "accuracy", accuracy
    print "precision",precision
    print "recall",recall
    print "f1",f1
    print "f2",f2
except:
    print  "SVM-RBF"
    print "Precision or recall may be undefined due to a lack of true positive predicitons."

print "true negatives",true_negatives
print "false negatives",false_negatives
print "false positives",false_positives
print "true positives",true_positives


#KNN

from sklearn.neighbors import KNeighborsClassifier

sss = StratifiedShuffleSplit(labels, n_iter = 1000,test_size = 0.3, random_state=42)
true_negatives = 0
false_negatives = 0
true_positives = 0
false_positives = 0

for train_idx, test_idx in sss:
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_idx:
        features_train.append( features[ii] )
        labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
    # train a classifier
    clf = KNeighborsClassifier(n_neighbors=10)
    clf.fit(features_train, labels_train)
    # test the classifier
    pred = clf.predict(features_test)
    for prediction, truth in zip(pred, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1
                   
    

try:
    total_predictions = true_negatives + false_negatives + false_positives + true_positives
    accuracy = 1.0*(true_positives + true_negatives)/total_predictions
    precision = 1.0*true_positives/(true_positives+false_positives)
    recall = 1.0*true_positives/(true_positives+false_negatives)
    f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
    f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
    print "KNN"
    print "accuracy", accuracy
    print "precision",precision
    print "recall",recall
    print "f1",f1
    print "f2",f2
except:
    print "KNN"
    print "Precision or recall may be undefined due to a lack of true positive predicitons."

print "true negatives",true_negatives
print "false negatives",false_negatives
print "false positives",false_positives
print "true positives",true_positives

# Logistic Regression
from sklearn.linear_model import LogisticRegression

sss = StratifiedShuffleSplit(labels, n_iter = 1000,test_size = 0.3, random_state=42)
true_negatives = 0
false_negatives = 0
true_positives = 0
false_positives = 0

for train_idx, test_idx in sss:
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_idx:
        features_train.append( features[ii] )
        labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
    # train a classifier
    clf = LogisticRegression()
    clf.fit(features_train, labels_train)
    # test the classifier
    pred = clf.predict(features_test)
    for prediction, truth in zip(pred, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1
                   
    

try:
    total_predictions = true_negatives + false_negatives + false_positives + true_positives
    accuracy = 1.0*(true_positives + true_negatives)/total_predictions
    precision = 1.0*true_positives/(true_positives+false_positives)
    recall = 1.0*true_positives/(true_positives+false_negatives)
    f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
    f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
    print "Logistic Regression"
    print "accuracy", accuracy
    print "precision",precision
    print "recall",recall
    print "f1",f1
    print "f2",f2
except:
     print "Precision or recall may be undefined due to a lack of true positive predicitons."     


                                    
### Tuning the classifier to achieve better than .3 precision and recall 

# Naive Bayes does not have parameters to tune

sss = StratifiedShuffleSplit(labels, n_iter = 1000,test_size = 0.3, random_state=42)
true_negatives = 0
false_negatives = 0
true_positives = 0
false_positives = 0

for train_idx, test_idx in sss:
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_idx:
        features_train.append( features[ii] )
        labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
    # train a classifier
    clf = GaussianNB()
    clf.fit(features_train, labels_train)
    # test the classifier
    pred = clf.predict(features_test)
    for prediction, truth in zip(pred, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1

try:
    total_predictions = true_negatives + false_negatives + false_positives + true_positives
    accuracy = 1.0*(true_positives + true_negatives)/total_predictions
    precision = 1.0*true_positives/(true_positives+false_positives)
    recall = 1.0*true_positives/(true_positives+false_negatives)
    f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
    f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
    print "Best Classifier - Naive Bayes"
    print "accuracy", accuracy
    print "precision",precision
    print "recall",recall
    print "f1",f1
    print "f2",f2
except:
     print "Precision or recall may be undefined due to a lack of true positive predicitons."




### Task 6: Dump the classifier, dataset, and features_list so anyone can
### check your results. 

dump_classifier_and_data(clf, my_dataset, final_features_list)