
test_set_filename = "KDD_Track2_solution.csv"

"""
Given list of CTR predictions for items in test set,
return the mean squared error of predictions using
actual CTR values from the test set
"""
def evaluator(list_of_predictions):
    f = open(test_set_filename, 'r')
    
    mean_squared_error = 0.0
    total_sum = 0.0
    for prediction in list_of_predictions:
	# read in item from test set
	fields = f.readline().split(',')
	#print fields
	    
	# actual value is clicks/impressions
	#print fields[0]
	#print fields[1]
	value = float(int(fields[0]))/float(int(fields[1]))

	#print (prediction, value)
	total_sum += (prediction - value) * (prediction - value)

    f.close()

    mean_squared_error = total_sum/len(list_of_predictions)
    return mean_squared_error 
	

