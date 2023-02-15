# Classification
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, FunctionTransformer
#Library in Model Selection class
from sklearn.metrics import roc_auc_score,average_precision_score,accuracy_score,recall_score,precision_score,f1_score,classification_report,log_loss,brier_score_loss,hamming_loss
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors    import KNeighborsClassifier
from sklearn.svm          import SVC, NuSVC
from sklearn.tree         import DecisionTreeClassifier
from sklearn.ensemble     import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier, ExtraTreesClassifier
from xgboost              import XGBClassifier
from catboost             import CatBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, RepeatedStratifiedKFold
from sklearn.model_selection import KFold, cross_val_score, RepeatedKFold
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, ElasticNetCV, Ridge
from sklearn.neighbors import KNeighborsRegressor

from sklearn.ensemble import GradientBoostingRegressor, ExtraTreesRegressor, AdaBoostRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error, max_error, mean_squared_log_error
from sklearn.model_selection import KFold
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import SGDRegressor, HuberRegressor,TheilSenRegressor, RANSACRegressor
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
from imblearn.pipeline import Pipeline
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.gaussian_process import GaussianProcessRegressor
class model_selection:
    """
    - Remove unnecessary features
    - Show a chart that compares the effectiveness of each method.
    - Based on the chart, choose the best method.

    Input:
    ------
    Rescaled Data_train and test
    X_train: np.array
    y_train: np.array
    SAVE_PREFIX: str
        direction to save data
    data_naMe: str
        Name of data type (MACCs, Mordred,...)
    task_type: str
        Classification (C) or Regression (R)
    scoring: str
        if task_type = (C): 'f1', 'average_precision', 'recall'
        if task_type = (R): 'r2', 'neg_mean_squared_error', 'neg_mean_absolute_error'
        
    
    Returns:
    --------
    Completed Data_train and Data_test
    df_mectrics: DataFrame
        Evaluation results of cross validation
    box_plot: fig
    """
    def __init__(self, X_train, y_train,SAVE_PREFIX, data_name, task_type ='C',scoring = 'f1'):
        self.X_train = X_train
        self.y_train = y_train
        self.SAVE_PREFIX =SAVE_PREFIX
        self.data_name =data_name
        self.task_type = task_type
        self.scoring = scoring
       
        self.results = list()
        self.names = list()
     # Check task type
        if len(self.y_train.unique())==2:
            self.task_type == 'C'
            self.cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=42)
            self.models,  self.names = self.Classification()
        else:
            self.task_type == 'R'
            self.cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=42)
            self.models,  self.names = self.Regression()

    # 1. Model Regression    
    def Regression(self):
        models, names = list(), list()
          
        #1. LR
        model = LinearRegression()
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('LR')
        
        #2. Ridge
        model = Ridge(alpha = 1, random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('Ridge')
        
        #3. ElasticNet
        model = ElasticNetCV(cv = 5, random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('ELN')
        
        #4. HuberRegressor
        model = HuberRegressor(max_iter = 10000)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('Huber')
        
        #5. PCR
        models.append(make_pipeline(StandardScaler(), PCA(n_components=10), LinearRegression()))
        names.append('PCR')
        
        #6. PLS
        model = PLSRegression(n_components=10)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('PLS')
        
        #7. GPR
        kernel = DotProduct() + WhiteKernel()
        model = GaussianProcessRegressor(kernel=kernel,random_state=42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('GPR')
        
        
        #8 KNN
        model = KNeighborsRegressor()
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('KNN')
        
        #9 svm
        model = SVR(kernel='rbf', gamma='scale', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('SVM')
        
        
        # 10 RF
        model = RandomForestRegressor(random_state=42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('RF')
        
        # 11 ExT
        model = ExtraTreesRegressor(random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('ExT')
        
        #16 ADA
        #model = AdaBoostRegressor(random_state = 42)
        #steps = [('m', model)]
        #models.append(Pipeline(steps=steps))
        #names.append('ADA')
        
        #12 Grad
        model = GradientBoostingRegressor(random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('Grad')
     
        #13 XGB
        model = XGBRegressor(random_state = 42, verbosity=0, use_label_encoder=False, eval_metrics ='logloss')
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('XGB')
        
        #14 Cat
        model = CatBoostRegressor(verbose = 0, random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('CatB')
        
        #15 Cat
        model = HistGradientBoostingRegressor(random_state = 42, verbose = 0)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('Hist')
        
        #16 MLP
        model = MLPRegressor(alpha = 0.01, max_iter = 10000, validation_fraction = 0.1, random_state = 42, hidden_layer_sizes = 150)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('MLP') 
        return models, names
    
    # 2. Model Classification  
    def Classification(self):
        models, names = list(), list()
        
        #0. Dummy
        #model = DummyClassifier(strategy='stratified', random_state =42)
        #steps = [('m', model)]
        #models.append(Pipeline(steps=steps))
        #names.append('Baseline')
        
        #1. Logistics
        model = LogisticRegression(penalty = 'l2', max_iter = 100000)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('Logistic')
        
        #2 KNN
        model = KNeighborsClassifier(n_neighbors = 20)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('KNN')
        
        #3 svm
        model = SVC(probability = True, max_iter = 10000)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('SVM')
        
       
        
        #9 RF
        model = RandomForestClassifier(random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('RF')
        
        #10 ExT
        model = ExtraTreesClassifier(random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('ExT')
        
        #11 ADA
        model = AdaBoostClassifier(random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('Ada')
        
        #12 Grad
        model = GradientBoostingClassifier(random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('Grad')
     
        #13 XGB
        model = XGBClassifier(random_state = 42, verbosity=0, use_label_encoder=False, eval_metrics ='logloss')
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('XGB')
        
        #14 Cat
        model = CatBoostClassifier(verbose = 0, random_state = 42)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('CatB')
        
        #15 MLP
        model = MLPClassifier(alpha = 0.01, max_iter = 10000, validation_fraction = 0.1, random_state = 42, hidden_layer_sizes = 150)
        steps = [('m', model)]
        models.append(Pipeline(steps=steps))
        names.append('MLP') 
        return models, names
    
    def evaluate_model(self, X, y, model):
      #Kết quả đánh giá model
        scores = cross_val_score(model, X, y, scoring=self.scoring, cv=self.cv, n_jobs=-1)
        return scores   
    
    def compare(self): 
      # Đưa tất cả các kết quả đánh giá vào list_results
        for i in range(len(self.models)):
            scores = self.evaluate_model(self.X_train, self.y_train, self.models[i])
            self.results.append(scores)
            print('>%s %.3f (%.3f)' % (self.names[i], np.mean(scores), np.std(scores)))
        #self.model_compare = statical_test(self.results, self.names,X_train = self.X_train, y_train = self.y_train)
        #self.model_compare.visualize()
        a = np.stack(self.results)
        self.df_metrics = pd.DataFrame(a.T, columns = self.names)
        self.df_metrics.to_csv(self.SAVE_PREFIX +self.data_name+"_model_selection.csv")
            
    def visualize(self):
      
        mean = list()
        for i in range (len(self.results)):
            x = self.results[i].mean().round(3)
            mean.append(x)
        data = np.array(mean)   
        ser = pd.Series(data, index =self.names)


        dict_columns = {'Mean':mean,'Method':self.names,}
        df = pd.DataFrame(dict_columns)


        sns.set_style("whitegrid")
        plt.figure(figsize=(20,10))
        box_plot = sns.boxplot(data=self.results,showmeans=True ,meanprops={"marker":"d",
                       "markerfacecolor":"white", 
                       "markeredgecolor":"black",
                      "markersize":"10"})
        #box_plot.axes.set_title("Compare feature selection method", fontsize=16)
        #box_plot.set_xlabel("Method", fontsize=14)
        box_plot.set_ylabel(f"{self.scoring}", fontsize=16)
        vertical_offset = df["Mean"].median()*0.01

        for xtick in box_plot.get_xticks():
            box_plot.text(xtick,ser[xtick]+ vertical_offset,ser[xtick], 
            horizontalalignment='center',color='w',weight='semibold', fontsize = 12)
    
        #box_plot.get_xticks(range(len(self.results)))
      
        box_plot.set_xticklabels(self.names, rotation='horizontal', fontsize = 16)
        #plt.savefig(self.SAVE_PREFIX+"model_selection.png", dpi = 600)
