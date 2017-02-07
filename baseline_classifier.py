import numpy as np
def find_unique_bank_entries_and_accounts(company_df):
    """Finding unique bank entries and unique accounts in the company database"""
    unique_bank_entry_text = company_df['BankEntryText'].unique()
    num_unique_bank_entries = unique_bank_entry_text.shape[0]
    unique_account_numbers = company_df['AccountNumber'].unique()
    num_unique_accounts = unique_account_numbers.shape[0]
    return (
        unique_bank_entry_text,
        num_unique_bank_entries,
        unique_account_numbers,
        num_unique_accounts
        )

def splitting_train_and_set(company_df):
    """Splitting the dataset into a train set and a test set. The split is 80% and 20%"""
    percent_train_size = 0.8
    data_size = company_df.shape[0]
    train_size = int(round(percent_train_size * data_size))
    test_size = int(data_size - train_size)
    train_df = company_df.tail(train_size)
    test_df = company_df.head(test_size)
    return (train_size, test_size, train_df, test_df)

def build_train_matrix(
        num_unique_bank_entries,
        num_unique_accounts,
        unique_account_numbers,
        unique_bank_entry_text,
        train_df
    ):
    """Building the matrix from the train data. This will be used to build the classifier."""
    train_matrix = np.zeros((num_unique_bank_entries, num_unique_accounts))
    unique_bank_entry_counter = 0
    for bank_entry in unique_bank_entry_text:
        temp_df = train_df[train_df.BankEntryText == bank_entry]
        temp_account_number = temp_df['AccountNumber']
        for account in temp_account_number:
            account_index = unique_account_numbers == account
            train_matrix[unique_bank_entry_counter, :] = train_matrix[unique_bank_entry_counter, :] + account_index
        unique_bank_entry_counter += 1
    return train_matrix

def calculate_accuracy(test_df, test_size, classifier):
    """Calculating the accuracy of the classifier."""
    account_test = np.zeros((test_size, 1))
    counter = 0
    for account_number in test_df['AccountNumber']:
        account_test[counter] = account_number
        counter += 1
    counter = 0
    account_predict = np.zeros((test_size, 1))
    for bank_entry_text in test_df['BankEntryText']:
        account_predict[counter] = classifier[bank_entry_text]
        counter += 1

    if test_size > 0:
        num_correct_predictions = float(sum(account_predict == account_test))
        accuracy = num_correct_predictions / test_size
    else:
        accuracy = 0
        num_correct_predictions = 0
    return (num_correct_predictions, accuracy)

def max_elements_in_train_matrix(train_matrix):
    """Finding the maximal element in each row of the training matrix."""
    max_element_idx = np.zeros(len(train_matrix))
    for row in range(0, len(train_matrix)):
        index = np.where(train_matrix[row, :] == max(train_matrix[row, :]))
        max_element_idx[row] = index[0][0]
    return max_element_idx

def build_classifier(
        unique_bank_entry_text,
        unique_account_numbers,
        max_element_idx
    ):
    """Build and return a dictionary with bank entry text as key and most
    frequently account number as value."""
    counter = 0
    classifier = {}
    for bank_entry in unique_bank_entry_text:
        classifier[bank_entry] = unique_account_numbers[max_element_idx[counter]]
        counter += 1
    return classifier

def baseline_classifier(company_df):
    """Builds and test the baseline classifier."""
    (
        unique_bank_entry_text,
        num_unique_bank_entries,
        unique_account_numbers,
        num_unique_accounts
     ) = find_unique_bank_entries_and_accounts(company_df)
    (
        train_size,
        test_size,
        train_df,
        test_df
    ) = splitting_train_and_set(company_df)
    train_matrix = build_train_matrix(
        num_unique_bank_entries,
        num_unique_accounts,
        unique_account_numbers,
        unique_bank_entry_text,
        train_df)
    max_element_idx = max_elements_in_train_matrix(train_matrix)
    classifier = build_classifier(
        unique_bank_entry_text,
        unique_account_numbers,
        max_element_idx
        )
    num_correct_predictions, accuracy = calculate_accuracy(test_df, test_size, classifier)
    return (train_size, test_size, num_correct_predictions, accuracy)
