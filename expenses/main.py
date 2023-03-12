from transactions import Transactions


def main(account, date_of_interest):
    transactions = Transactions(account, date_of_interest)

    df = transactions.read_input(transactions.input_path, "input.csv", ";")
    df = transactions.preprocess(df)
    df = transactions.split_up_date(df)
    df = transactions.filter_on_month_of_interest(df)
    output_path = transactions.get_output_path(df)
    transactions.write_output(df, output_path, f"{date_of_interest}_output.xlsx")


if __name__ == "__main__":
    main(
        account="lisa_william",
        date_of_interest="2022-11"
        )
