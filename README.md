# Categorical Correlation
A simple wrapper for some useful correlation/association metrics for categorical/nominal variables.

Available metrics:
- Cramer's V
- Tschuprow's T
- Pearson Contingency Value
- Theil's U (assymetric)

# Example
Let's use some random categorical data as an example:

```
import pandas as pd
import numpy as np

data = pd.util.testing.makeCustomDataframe(
    nrows=10000,
    ncols=10,
    dtype='category',
    data_gen_f=lambda *args: np.random.randint(5)
)
```

Then, let's generate the cramer correlation matrix.

```
import cat_corr as cat
res = cat.get_categorical_corr(
    data=data,
    features=data.columns,
    method='cramer',
    thr=0.5
)

cramer_corr_matrix = res[0]
```


# Requirements
- pandas >= 1.0.0
- numpy >= 1.21.2
- scipy >= 1.7.1
- dython >= 0.7.1.post3
