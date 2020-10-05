# -*- coding: utf-8 -*-
"""hypothyroid classification .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11Ei_sO_6d9Erb84yjE3eweEYZVLpRZHN

# Main goal for the analysis

The main objective  of the analysis is to build a predictive model which is very accurate to predict if a patient is suffering from Hypothyroid or not.
Using various test done at the hospital, one will be be able to predict if a patient is suffering from the illness or not.

# **Metric of success**

This analysis will be considered a success when we are able to apply Various ensemble classifers and SVM classifer to the dataset in order to identify the best prediction model that has the highest accuracy level. The baseline model should be identified and compared to other classiffication models. The prediction model selected for this research question should not suffer from any instances of overfitting or underfitting.

## Understanding the context

Hypothyroidism is a condition in which the thyroid gland doesn't produce enough thyroid hormone. Thyroid glands is a butterfly shaped glands under the adam's apple.
Hypothyroidism's deficiency of thyroid hormones can disrupt such things as heart rate, body temperature and all aspects of metabolism. Hypothyroidism is most prevalent in older women.
Major symptoms include fatigue, cold sensitivity, constipation, dry skin and unexplained weight gain

Nairobi Hospital conducted a free clinical camp to carry out a hypothroidism test, the clinical officers focused on thyroid patient to get the necessary data.

The patients went through 18 tests, to help doctors determine if the patient have the condition or not.

From the data collected by the clinical officers during the camp, it would be very useful to us to build a model that is able to classify the patient as a sick or not sick

# Recording the Experimental Design

To conduct the analysis successfully , the following steps will be followed:


1.   Loading the dataset
2.   Data understanding

1.   Data cleaning and manipulation
2.   Exploratory Data analysis

1.   Predictive analysis
2.   Implementing the solution

# **Data relevance**

The data was collected by clinical officers during a clinical camp held in Nairobi Hospital.
some of the data collected included ;

age, , on_thyroxine ,query_on_thyroxine	,on_antithyroid_medication,	thyroid_surgery,	query_hypothyroid,	query_hyperthyroid,	pregnant,	sick,	tumor,	lithium	goitre,	TSH_measured,		T3_measured,		TT4_measured,		T4U_measured,		FTI_measured,		TBG_measured,
"""

## import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.model_selection import KFold,GridSearchCV
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,mean_squared_error
import warnings
warnings.filterwarnings('ignore', '.*do not.*',)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from sklearn.svm import SVC

"""# **Data Understanding**"""

## import the csv file
data=pd.read_csv('/content/hypothyroid.csv')

## first few rows of the data
data.head()

## last few rows
data.tail()

### the number of columns and rows
data.shape

## the data type of each column
data.info()

"""All the columns in our data set are object, even the numerical data, hence will need to clean that and convert them into floats and integers

# Data cleaning and manipulation
"""

### checking for missing values
data.isnull().sum()

"""In the dataset we have missing values, the missing values are labelled with a '?', hence our code above is not able to read that... example some of the patient did not provide their age, other patient did not take some test"""

### TBG has anormaly which is a ?  meaning  it is not measured, 
data['TBG'].unique()

## investigate the number of ? in the column
data[data['TBG']=='?'].count()

data.head()

## replacing the missing values  with 0 so that we can convert them into floats
col_num=['TBG','T3','T4U','TSH','TT4','FTI','age']
for t in col_num:
  data[['TBG','T3','T4U','TSH','TT4','FTI','age']]=data[col_num].replace('?','0')

# converting the necessary objects into float
 data[['TBG','T3','T4U','TSH','TT4','FTI']]=data[['TBG','T3','T4U','TSH','TT4','FTI',]].astype(float)
 data.info()

### replace ? in sex with others
data['sex']=data['sex'].str.replace('?','not provided')

### converting age into int
data['age']=data['age'].str.replace('?','0')
data['age']=data['age'].astype(int)

### replace f with false and t with true for better visualization
col=['status','age','sex','on_thyroxine','query_on_thyroxine','on_antithyroid_medication','thyroid_surgery','query_hypothyroid',
      'query_hyperthyroid','pregnant','sick','tumor','lithium','goitre','TSH_measured','TSH','T3_measured','T3','TT4_measured','TT4','T4U_measured','T4U',
      'FTI_measured','FTI','TBG_measured','TBG']
for i in col:
  data=data[col].replace('f','false').replace('t','true').replace('n','no').replace('y','yes')
data.head()

#### looking for duplicates
data.duplicated().value_counts()

### dropping the duplicated figures
data.drop_duplicates()

### looking for outliers
fig,((ax1,ax2),(ax3,ax4),(ax5,ax6))=plt.subplots(3,2,figsize=(10,10))
plt.suptitle('looking for outliers',fontsize=(15))
sns.boxplot(data['FTI'],ax=ax1,color='red')
sns.boxplot(data['TT4'],ax=ax2,color='yellow')
sns.boxplot(data['TSH'],ax=ax3,color='skyblue')
sns.boxplot(data['TBG'],ax=ax4,color='green')
sns.boxplot(data['T4U'],ax=ax5,color='pink')
sns.boxplot(data['T3'],ax=ax6,color='olive')
plt.show()

#### q1 and q3
q1=data.quantile(0.25)
q3=data.quantile(0.75)
IQR=q3-q1

### printing out the specific outliers per column
print(IQR)

## removing the outliers
data=data[~((data<(q1-1.5*IQR))|(data>(q3+1.5*IQR))).any(axis=1)]
data.shape

#### Finally a cleaning the data
data.head()

"""# Exploratory data analysis"""

## descriptive statistics
data.describe()

###  frequency plots
col_names = ['TSH', 'T3', 'TT4', 'T4U', 'FTI','TBG','age']
fig, ax = plt.subplots(len(col_names), figsize=(10,20))

for i, col_val in enumerate(col_names):

    sns.distplot(data[col_val], hist=True, ax=ax[i])
    ax[i].set_title('Frequency distribution of '+col_val, fontsize=10)
    ax[i].set_xlabel(col_val, fontsize=8)
    ax[i].set_ylabel('Count', fontsize=8)

plt.show()

### finding mode,median,kurtosis, and skewness
col_names = ['TSH', 'T3', 'TT4', 'T4U', 'FTI','TBG','age']
for i in col_names:
  median=data[col_names].median()
  skewness=data[col_names].skew()
  kurtosis=data[col_names].kurt()
  mode=data[col_names].mode()
  print('median:',median)

  print('skewness:',skewness)

  print('kurtosis:',kurtosis)

  print('mode',mode)

  break

## subplots to show count
fig,((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8),(ax9,ax10),(ax11,ax12))=plt.subplots(6,2,figsize=(16,16))
sns.countplot('status',hue='sex',data=data,palette='magma',ax=ax1)
sns.countplot('status',hue='on_thyroxine',data=data,palette='Set1',ax=ax2)
sns.countplot('status',hue='query_on_thyroxine',data=data,palette='Set2',ax=ax3)
sns.countplot('status',hue='on_antithyroid_medication',data=data,palette='flare',ax=ax4)
sns.countplot('status',hue='thyroid_surgery',data=data,palette='YlOrRd',ax=ax5)
sns.countplot('status',hue='goitre',data=data,palette='husl',ax=ax6)
sns.countplot('status',hue='query_hypothyroid',data=data,palette='pastel',ax=ax7)
sns.countplot('status',hue='query_hyperthyroid',data=data,palette='deep',ax=ax8)
sns.countplot('status',hue='pregnant',data=data,palette='GnBu',ax=ax9)
sns.countplot('status',hue='sick',data=data,palette='OrRd',ax=ax10)
sns.countplot('status',hue='tumor',data=data,palette='PuBu',ax=ax11)
sns.countplot('status',hue='lithium',data=data,palette='YlOrBr',ax=ax12)
for p in ax1.patches:
  ax1.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax2.patches:
  ax2.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax3.patches:
  ax3.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax4.patches:
  ax4.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax5.patches:
  ax5.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax6.patches:
  ax6.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax7.patches:
  ax7.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax8.patches:
  ax8.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax9.patches:
  ax9.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax10.patches:
  ax10.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax11.patches:
  ax11.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax12.patches:
  ax12.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', 
              va = 'center', xytext = (0, 10), textcoords = 'offset points')

### doing the  correlation of the data
## encoding the data
ll=LabelEncoder()
df=pd.DataFrame()
for i in data.columns:
  df[i]=ll.fit_transform(data[i])
df.head()
### correlation
fig,plt.figure(figsize=(20,12))
sns.heatmap(df.corr(),annot=True,vmax=1,vmin=0)

"""# Predictive Analysis"""

#### split the data the data into features and label
y=np.array(df['status'])
features_list=df.drop('status',1).columns
x=np.array(df.drop('status',1))

#### normalization
ss=StandardScaler()
x=ss.fit_transform(x)

### splitting the data training and test set
fold=KFold(n_splits=5)
count=1
for train_index,test_index in fold.split(x):
  print('training model',count)
x_train,x_test=x[train_index],x[test_index]
y_train,y_test=y[train_index],y[test_index]

"""## Random forest"""

### random forest
msitu=RandomForestClassifier(n_estimators=1000,max_depth=10,min_samples_split=2,min_samples_leaf=1,verbose=1)
forest=msitu.fit(x_train,y_train)
forest

### predict
y_pred=msitu.predict(x_test)
### checking the prediction
pd.DataFrame({'actual':y_test.flatten(),'predicted':y_pred.flatten()})

### checking the performance
print('accuracy:-',accuracy_score(y_test,y_pred))
print('MSE:-',mean_squared_error(y_test,y_pred))

from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus

dot_data = StringIO()
# pick a specific tree from the forest
tree = msitu.estimators_[50]

export_graphviz(tree, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = features_list)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('mti.png')
Image(graph.create_png())

"""Our  Random forest had a very high accuracy of 99.3%, considering this is a medical prediction, a high accuracy is paramount to avoid any error that can lead to mis-diagonosis.
From a our tree we can see FTI measured  was our Root node, with a gini score of 0.102 which is very small. 
From the root node  1500 samples were tested and 136 were positive..

## GradientBoosting Classifer
"""

## fitting
gb=GradientBoostingClassifier(n_estimators=1000,learning_rate=0.8,max_depth=5,min_samples_split=2,min_samples_leaf=1)
gb.fit(x_train,y_train)

#### predicting
y_pred=gb.predict(x_test)
pd.DataFrame({'actual':y_test.flatten(),'predicted':y_pred.flatten()})

#### checking the accuracy
print('accuracy:-',accuracy_score(y_test,y_pred))
print('MSE:-',mean_squared_error(y_test,y_pred))

"""The Gradient boosting classifer had an accuracy score of 99.37% same with the random forest

## Support Vector machine
"""

### polynomial SVM
poly=SVC(kernel='poly',gamma='auto',degree=3)
poly.fit(x_train,y_train)

## predicting
y_pred=poly.predict(x_test)
pd.DataFrame({'actual':y_test.flatten(),'predict':y_pred.flatten()})

###3 checking the accuracy of the model
print('accuracy:-',accuracy_score(y_test,y_pred))
print('MSE:-',mean_squared_error(y_test,y_pred))

###Fitting the model: Radial basis function (rbf)
rbf=SVC(kernel='rbf',degree=2,gamma='auto')
rbf.fit(x_train,y_train)

####predicting
y_pred=rbf.predict(x_test)
pd.DataFrame({'actual':y_test.flatten(),'predict':y_pred.flatten()})

### accuracy
print('accuracy:-',accuracy_score(y_test,y_pred))
print('MSE:-',mean_squared_error(y_test,y_pred))

### fitting linear
linear=SVC(kernel='linear',gamma='auto',degree=3)
linear.fit(x_train,y_train)

##predict
y_pred=linear.predict(x_test)

### accuracy
print('accuracy:-',accuracy_score(y_test,y_pred))
print('MSE:-',mean_squared_error(y_test,y_pred))

"""# **Challenging the solution**

Below is the summary of the accuracy scores for the models investigated in this analysis:

Random forest - 99.37%

Gradient boosting classifer - 99.37%

SVM(polynomial) -99.56%

SVM(linear) - 99.21%

SVM(rbf) - 99.37%

From the above we can see that SVM polynomial had the highest accuracy, although  all the models had a very ahigh accuracy. I would recommend we use any of the above models since 99% is a high Accuracy for any model.

# Follow-up Questions

## a) Did we have the right data?

Yes we had: the data provided all the necessary information to classify a patient sick or not

## b)Do we need other data to answer the research question

Yes, since this is a medical research more samples would help improve our model, and help it learn more, three thousand samples are not enough

## c) Did we have the right question?

The research question was sufficient and helped to hit the objective of the analysis
"""