# Project : LansWeeper
# Created by Moncef BENAICHA at 7/24/18 - 21:50
# Email : contact@moncefbenaicha.me

from LansWeeper import LansWeeper
import pandas as pd


def main():
    lansweeper = LansWeeper("http://localhost:81/")
    assests = lansweeper.getAssestsLInks()
    data = []
    for link in assests[1:]:
        try:
            data.append(lansweeper.getAssestsData(link))
        except:
            continue
    print(f'{ len(data) } item(s) found.')
    dataframe = pd.DataFrame(data)
    dataframe.to_csv("data.csv", index=False)


if __name__ == '__main__':
    main()
