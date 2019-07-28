
import pandas as pd


def addNullModel(data):
    data.reset_index(inplace=True)
    data.columns = ['valor', 'data']
    data['data'] = data['data'].dt.to_period('M')
    return data 

# SARIMA MODEL AUTOMATION
def modellingSARIMA(data, target, pred_intervals):

    # importar modelo
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    # executar modelo
    model = SARIMAX(data[target], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    model_fit = model.fit(disp=False)

    # previsoes para proximos pred_intervals 
    predicted = model_fit.predict(len(data), (len(data)+pred_intervals) )   

    # retornar valores preditos
    return predicted 


# HOLT WINTERS MODEL AUTOMATION
def modellingHW(data, target, pred_intervals):

    # importar modelo
    from statsmodels.tsa.api import ExponentialSmoothing

    # executar modelo
    fit4 = ExponentialSmoothing(data[target], 
                                seasonal_periods=12, 
                                trend='add', 
                                seasonal='mul', 
                                damped=True).fit(use_boxcox=True)
    predicted = fit4.forecast((pred_intervals+1)).rename(r'$\alpha=%s$'%fit4.model.params['smoothing_level'])

    # retornar valores preditos
    return predicted 


# PREDICTION DATA GENERATOR
def predictionData(data, target, start_date, end_date, model_choice = 'SARIMA'):
    
    import pandas as pd

    # make interval of date
    interval = pd.date_range(start=start_date, end=end_date, freq='MS') 
    pred_intervals = (len(interval)-1)   

    # MODEL CHOICE
    if model_choice == 'SARIMA':
        print('SARIMA Model Running')
        predicted = modellingSARIMA(data, target, pred_intervals)
    elif model_choice == 'HW':
        print('HOLT WINTERS Model Running')
        predicted = modellingHW(data, target, pred_intervals)
    else:
        print("Model choice not available, choose 'SARIMA' or 'HW' (HOLT WINTERS)")

    # make date to prediction
    prediction = pd.DataFrame(interval, predicted)
    prediction = addNullModel(prediction)

    # rename target columns and merge outer
    data.columns = ['data', 'valor']
    datapred = pd.merge(data, prediction, how = 'outer', on = 'data')

    # save dataframe
    datapred.to_csv( ('resultados/tabelas/'+target+'_'+model_choice+'.csv') , index=False, encoding='utf-8' )
    print('Prediction data successfully saved! :)')



