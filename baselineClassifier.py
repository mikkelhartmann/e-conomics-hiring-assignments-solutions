def baselineClassifier(company_df):
    import numpy as np 

    BankEntryText = company_df['BankEntryText'].unique()
    numUniqueBankEntries = BankEntryText.shape[0]
    AccountNumber = company_df['AccountNumber'].unique()
    numUniqueAccounts = AccountNumber.shape[0]

    percentTrainSize = 0.8
    trainSize = int(round(percentTrainSize*company_df.shape[0]))
    testSize = int(company_df.shape[0]-trainSize) 

    train_df = company_df.tail(trainSize)
    test_df = company_df.head(testSize)

    # Build the matrice on the train set
    trainMatrix = np.zeros((numUniqueBankEntries,numUniqueAccounts))
    kk = 0
    for bankEntry in BankEntryText:
        temp_df = train_df[train_df.BankEntryText == bankEntry]
        iteration = temp_df['AccountNumber']
        for item in iteration:
            accountIndex = AccountNumber == item
            trainMatrix[kk,:] = trainMatrix[kk,:] + accountIndex
        kk += 1
        
    # Find the maximal element in the matrice and save a dictionary that contains BankEntry string and Account number
    indices = np.zeros(len(trainMatrix))
    for row in range(0,len(trainMatrix)):
        index = np.where(trainMatrix[row,:]==max(trainMatrix[row,:]))
        indices[row] = index[0][0]
        #trainMatrix[row,index][0][0]

    # Making the dictionary
    kk=0
    bankEntryTextToAccountNumber = {}
    for bankEntry in BankEntryText:
        bankEntryTextToAccountNumber[bankEntry] = AccountNumber[indices[kk]]
        kk += 1

    y_test = np.zeros((testSize,1))
    kk = 0
    for account in test_df['AccountNumber']:
        y_test[kk] = account
        kk += 1
        
    kk = 0
    y_predict = np.zeros((testSize,1))
    for text in test_df['BankEntryText']:
        y_predict[kk] = bankEntryTextToAccountNumber[text]
        kk += 1

    if testSize>0:
        numCorrect = float(sum(y_predict==y_test))
        accuracy = numCorrect/testSize
    else:
        accuracy = 0
        numCorrect = 0

    #print('Number of test cases is: ' + str(testSize))
    #print('number of correct predictions is: ' + str(numCorrect))
    #print('The accuracy is: ' + str(accuracy))

    return(testSize,numCorrect,accuracy)

