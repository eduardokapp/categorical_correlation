'''A wrapper for some useful categorical correlation/association metrics.'''

from itertools import combinations, permutations
from typing import List, Tuple

import pandas as pd
import numpy as np
from scipy.stats.contingency import association
from dython.nominal import theils_u


def get_categorical_corr(
    data: pd.DataFrame,
    features: List[str] = None,
    method: str = 'cramer',
    thr: float = 0.5
) -> Tuple[pd.DataFrame, dict]:
    """
    Given a dataframe and a list of categorical features, returns a correlation
    matrix, with correlation values for every feature pair. Along with the
    correlation matrix, a dictionary linking each feature that has a
    correlation with any other feature higher
    than `thr` value is also returned.

    Parameters
    ----------
        data: pd.DataFrame
            A DataFrame with categorical features of interest.
        features: List[str], optional, default=data.columns
            A list with feature names. If none is provided, will use all the
            columns in `data`.
        method: str, optional, default='cramer'
            The association metric to be used. Available methods:
                - 'cramer' (Cramer's V)
                - 'tschuprow' (Tschuprow's T)
                - 'pearson' (Pearson Contingency Value)
                - 'theil' (Theil's U assymetric association value)
        thr: float, optional, default=0.5
            A threshold value to return the correlated features dictionary.

    Returns
    -------
        The correlation matrix itself and the correlated features dictionary,
        as a tuple.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("'data' should be a pd.DataFrame.")
    if features is None:
        features = data.columns
    if not isinstance(features, list):
        raise TypeError("'features' should be a list with feature names.")
    if any(not isinstance(feature, str) for feature in features):
        raise TypeError("All elements inside 'features' should be strings.")
    if method not in ['cramer', 'tschuprow', 'pearson', 'theil']:
        raise TypeError("Unexpected method provided.")
    if not isinstance(thr, float):
        raise TypeError("'thr' should be a float value.")

    if method != 'theil':
        output = get_symmetrical_metric(data[features], method)
    else:
        output = get_asymmetrical_metric(data[features], method)

    # finding features that have any metric greater than 'thr'
    high_corr = [
        x for x in features if any(np.greater(output[x].drop(x, axis=0), thr))
    ]
    corr_features = {}
    features = np.array(features)
    for var in high_corr:
        cond = np.greater(output[f'{var}'], thr)
        not_itself = features != var
        corr_features[f'{var}'] = features[np.where(cond & not_itself)]

    return output, corr_features


def get_symmetrical_metric(data: pd.DataFrame, method: str) -> pd.DataFrame:
    """
    Given a dataframe and a list of categorical features, returns a correlation
    matrix, with correlation values for every feature pair.

    Parameters
    ----------
        data: pd.DataFrame
            A DataFrame with categorical features of interest.
        method: str
            The association metric to be used. Available symmetrical methods:
                - 'cramer' (Cramer's V)
                - 'tschuprow' (Tschuprow's T)
                - 'pearson' (Pearson Contingency Value)

    Returns
    -------
        A correlation matrix.
    """

    # result will be a n_features by n_features symmetric matrix
    # so we initialize it as an identity matrix
    output = pd.DataFrame(
        np.eye(len(data.columns)),
        columns=data.columns,
        index=data.columns
    )

    # because these metrics are symmetric, we only need half
    # of the pair-wise combinations
    combs = combinations(data.columns, r=2)
    # for every pair, we calculate its contingency based association.
    for comb in combs:
        feat_a = comb[0]
        feat_b = comb[1]

        # use crosstab to find the contingency table between features
        input_tab = pd.crosstab(data[feat_a], data[feat_b])
        res = association(input_tab, method=method, correction=True)

        output[feat_a][feat_b], output[feat_b][feat_a] = res, res

    return output


def get_asymmetrical_metric(data: pd.DataFrame, method: str) -> pd.DataFrame:
    """
    Given a dataframe and a list of categorical features, returns a correlation
    matrix, with correlation values for every feature pair.

    Parameters
    ----------
        data: pd.DataFrame
            A DataFrame with categorical features of interest.
        method: str
            The association metric to be used. Available asymmetrical methods:
                - Theil's U

    Returns
    -------
        A correlation matrix.
    """
    # result will be a n_features by n_features symmetric matrix
    # so we initialize it as an identity matrix
    output = pd.DataFrame(
        np.eye(len(data.columns)),
        columns=data.columns,
        index=data.columns
    )

    # because these metrics are asymmetric, we need all
    # of the pair-wise combinations
    combs = permutations(data.columns, r=2)
    # for every pair, calculate theil U.
    for comb in combs:
        feat_a = comb[0]
        feat_b = comb[1]

        output[feat_a][feat_b] = theils_u(
            data[feat_a],
            data[feat_b]
        )

    return output
