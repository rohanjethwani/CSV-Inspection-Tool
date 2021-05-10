import traceback
import pandas as pd


def perform_operations_on_csv(**kwargs):
    try:
        report = kwargs.get("report")
        view_columns = kwargs.get("view_columns", "ALL")
        group_column = kwargs.get("group_column", None)
        filter_column = kwargs.get("filter_column", None)
        filter_value = kwargs.get("filter_value", None)
        operation_column = kwargs.get("operation_column", None)
        operation_value = kwargs.get("operation_value", None)

        print("=================================")
        print("Report : ", report)
        print("View Columns : ", view_columns)
        print("Group Column : ", group_column)
        print("Filter Column : ", filter_column)
        print("Filter Value : ", filter_value)
        print("Operation Column : ", operation_column)
        print("Operation Value : ", operation_value)
        print("=================================")

        # Print CSV contents
        csv_contents = pd.read_csv(report)
        print("CSV File is read.")
        print("Columns : ", csv_contents.columns)
        display_contents(csv_contents, view_columns)

        # Apply grouping of columns
        group_column_csv_content = None
        if group_column:
            group_column_csv_content = group_columns(csv_contents, group_column)

        # Apply filtering on CSV
        filtered_csv_content = None
        if filter_column and filter_value:
            filtered_csv_content = apply_filter(
                group_column_csv_content if group_column_csv_content is not None else csv_contents, filter_column,
                filter_value)
            display_contents(filtered_csv_content, view_columns)

        # Apply operations on columns
        operation_csv_content = None
        data_frame = filtered_csv_content if filtered_csv_content is not None else group_column_csv_content if group_column_csv_content is not None else csv_contents
        if operation_column and operation_value:
            operation_csv_content = apply_operations(data_frame, operation_column, operation_value)
            display_contents(operation_csv_content, view_columns)

    except:
        traceback.print_exc()
        raise Exception("Failing Job")


def display_contents(data_frame, view_columns):
    try:
        if view_columns in ['ALL']:
            print(data_frame)
        else:
            print(data_frame[view_columns])
    except Exception:
        print("Status : FAIL")
        raise Exception("Error while displaying columns of the file.")


def group_columns(data_frame, group_columns):
    try:
        group_content = data_frame.groupby(group_columns)
        print("=================================")
        print("Grouping columns - ", group_columns)
        return group_content
    except Exception:
        print("Status : FAIL")
        raise Exception("Error while grouping columns of the file.")


def apply_filter(data_frame, filter_column, filter_value):
    try:
        filtered_content = data_frame[data_frame[filter_column] == filter_value]
        print("=================================")
        print("Filter applied on the data frame.")
        return filtered_content
    except Exception:
        print("Status : FAIL")
        raise Exception("Error while applying filter to the columns of the file.")


def apply_operations(data_frame, operation_column, operation_value):
    try:
        if operation_value == "SUM":
            operation_content = data_frame[operation_column].sum();
        elif operation_value == "MIN":
            operation_content = data_frame[operation_column].min();
        elif operation_value == "MAX":
            operation_content = data_frame[operation_column].max();
        elif operation_value == "MEAN":
            operation_content = data_frame[operation_column].mean();
        else:
            print("Operation not supported.")

        print("=================================")
        print("Operation applied on the data frame.")
        return operation_content
    except Exception:
        print("Status : FAIL")
        raise Exception("Error while applying operation to the columns of the file.")
