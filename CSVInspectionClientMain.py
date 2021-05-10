import datetime
import os
import sys
import argparse

from OperationsOnCSV import perform_operations_on_csv

def valid_date(dt):
    try:
        datetime.strptime(dt, "%Y%m%d")
        return dt
    except ValueError:
        message = "Not a valid date: '{0}'. Expected format is YYYYmmdd.".format(dt)
        raise argparse.ArgumentTypeError(message)


def parse_args(argv):
    operation_value_choices = ["SUM", "MIN", "MAX", "MEAN"]

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--report"
                        , required=True
                        , dest="report"
                        , help="Absolute path of the report on which operations to be performed."
                        )

    parser.add_argument("-vc", "--viewColumns"
                        , required=False
                        , dest="view_columns"
                        , nargs="*"
                        , help="Columns of the report to be viewed. Default is to view ALL columns. "
                                "To view specific columns, mention the column names (Example: Column1 Column2 Column3)."
                        )

    parser.add_argument("-gc", "--groupColumn"
                        , required=False
                        , dest="group_column"
                        , nargs="*"
                        , help="Column name on which grouping to be applied."
                        )

    parser.add_argument("-fc", "--filterColumn"
                        , required=False
                        , dest="filter_column"
                        , help="Column name on which filter to be applied."
                        )

    parser.add_argument("-fv", "--filterValue"
                        , required=False
                        , dest="filter_value"
                        , help="Value with which filter to be applied."
                        )

    parser.add_argument("-oc", "--operationColumn"
                        , required=False
                        , dest="operation_column"
                        , nargs="*"
                        , help="Column name on which operation to be applied."
                        )

    parser.add_argument("-ov", "--operationValue"
                        , required=False
                        , dest="operation_value"
                        , help="Value with which operation to be applied. Possible values are {0}.".format(operation_value_choices)
                        )

    args = parser.parse_args(argv)

    ###
    # Validation of input parameters
    ###
    if((args.filter_column is None and args.filter_value is not None)
            or (args.filter_column is not None and args.filter_value is None)):
        parser.error("Either mention both the parameters or none - filterColumn/fc and filterValue/fv.")

    if ((args.operation_column is None and args.operation_value is not None)
            or (args.operation_column is not None and args.operation_value is None)):
        parser.error("Either mention both the parameters or none - operationColumn/oc and operationValue/ov.")

    if args.group_column is not None and (args.filter_column is not None or args.filter_value is not None):
        parser.error("Either group columns or apply filter. Both are not allowed.")

    if args.group_column is not None and (args.operation_column is None or args.operation_value is None):
        parser.error("In order to apply grouping, operation columns and operation value must be provided.")

    if args.operation_value and args.operation_value not in operation_value_choices:
        parser.error("ov or operationValue must be one of these values - {0}".format(','.join(operation_value_choices)))

    return args.report, \
           args.view_columns, args.group_column, args.filter_column, args.filter_value, \
           args.operation_column, args.operation_value


def defined_kwargs(**kwargs):
    return {k: v for k,v in kwargs.items() if v is not None}


def main(argv):
    report, view_columns, group_column, filter_column, filter_value, operation_column, operation_value = parse_args(argv)

    try:
        perform_operations_on_csv(**defined_kwargs(report=report, view_columns=view_columns, group_column=group_column,
                                                   filter_column=filter_column, filter_value=filter_value,
                                                   operation_column=operation_column, operation_value=operation_value))

    except:
        print("Exiting with status code 1")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])


