Put all the .py files in the same folder

To run BestPossibleStrategy, simply do:
python BestPossibleStrategy.py

It will call testPolicy function and return a df_trade data frame, and then
generate needed information (graph, cumulative return, daily return std, daily return mean)

To run ManualStrategy, simply do:
python ManualStrategy.py

It will call testPolicy function and return a df_trade data frame, and generate
the same things as BestPossibleStrategy.py


You can also test testPolicy() of BestPossibleStrategy and ManualStrategy separately,
by importing BestPossibleStrategy as bps, you can call
bps.testPolicy(symbol, sd, ed) ... as specified on the website.
And similarly ManualStrategy.
